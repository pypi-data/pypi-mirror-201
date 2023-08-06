import copy
import math
import random
import time
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from threading import Lock

import numpy as np
import pandas as pd
import io
import os
import zipfile
import requests

from quantplay.exception.exceptions import QuantplayOrderPlacementException
from quantplay.utils.constant import Constants
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.utils.number_utils import NumberUtils
from quantplay.utils.pickle_utils import PickleUtils

logger = Constants.logger

class Broker():

    def __init__(self):
        self.instrument_id_to_symbol_map = dict()
        self.instrument_id_to_exchange_map = dict()
        self.instrument_id_to_security_type_map = dict()
        self.exchange_symbol_to_instrument_id_map = defaultdict(dict)
        self.order_type_sl = "SL"
        self.nfo_exchange = "NFO"

        self.orders_column_list = ['order_id', 'user_id', 'tradingsymbol', 'tag', 'average_price', 'transaction_type',
                                   'status', 'ltp', 'exchange', 'product', 'quantity', 'filled_quantity',
                                   'pending_quantity', 'order_timestamp']
        self.positions_column_list = ['tradingsymbol', 'quantity', 'ltp', 'pnl', 'buy_quantity',
                                      'sell_quantity', 'exchange', 'product', 'option_type']
        self.trigger_pending_status = "TRIGGER PENDING"
        self.lock = Lock()

    def initialize_symbol_data(self, save_as=None):
        instruments = self.instrument_data
        instruments = instruments.to_dict('records')
        self.symbol_data = {}
        for instrument in instruments:
            exchange = instrument['exchange']
            tradingsymbol = instrument['broker_symbol']

            instrument_data = copy.deepcopy(instrument)
            self.symbol_data["{}:{}".format(exchange, tradingsymbol)] = instrument_data

        PickleUtils.save_data(self.symbol_data, save_as)

    def initialize_broker_symbol_map(self):
        self.broker_symbol_map = {}
        for a in self.symbol_data:
            self.broker_symbol_map[self.symbol_data[a]['broker_symbol']] = self.symbol_data[a]['tradingsymbol']
        self.quantplay_symbol_map = {v: k for k, v in self.broker_symbol_map.items()}

    def round_to_tick(self, number):
        return round(number * 20) / 20

    def populate_instruments(self, instruments):
        """Fetches instruments for all exchanges from the broker
        and stores them in the member attributes.
        """
        Constants.logger.info("populating instruments")
        for instrument in instruments:
            exchange, symbol, instrument_id = (
                instrument.exchange,
                instrument.symbol,
                instrument.instrument_id,
            )
            self.instrument_id_to_symbol_map[instrument_id] = symbol
            self.instrument_id_to_exchange_map[instrument_id] = exchange
            self.instrument_id_to_security_type_map[
                instrument_id
            ] = instrument.security_type()
            self.exchange_symbol_to_instrument_id_map[exchange][symbol] = instrument_id

    def add_quantplay_fut_tradingsymbol(self):
        seg_condition = [
            ((self.instrument_data["instrument"].str.contains("FUT")) & (
                    self.instrument_data.instrument != "OPTFUT"))
        ]

        tradingsymbol = [
            self.instrument_data.tradingsymbol + self.instrument_data.expiry_year + self.instrument_data.month + "FUT"
        ]

        self.instrument_data.loc[:, "tradingsymbol"] = np.select(
            seg_condition, tradingsymbol, default=self.instrument_data.tradingsymbol
        )

    def add_quantplay_opt_tradingsymbol(self):
        seg_condition = (self.instrument_data["strike_price"] > 0)
        weekly_option_condition = (
                (self.instrument_data.expiry.dt.month == self.instrument_data.next_expiry.dt.month) & (
                self.instrument_data.exchange == "NFO"))
        month_option_condition = (
                (self.instrument_data.expiry.dt.month != self.instrument_data.next_expiry.dt.month) | (
                self.instrument_data.exchange == "MCX"))

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.expiry_year,
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & weekly_option_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.week_option_prefix,
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & month_option_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.month,
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol +
            self.instrument_data.strike_price.astype(float).astype(str).str.split(".").str[0],
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.option_type,
            self.instrument_data.tradingsymbol
        )

    def get_df_from_zip(self, url):
        response = requests.get(url, timeout=10)
        z = zipfile.ZipFile(io.BytesIO(response.content))

        directory = '/tmp/'
        z.extractall(path=directory)
        file_name = url.split(".txt")[0].split("/")[-1]
        os.system('cp /tmp/{}.txt /tmp/{}.csv'.format(file_name, file_name))
        time.sleep(2)
        return pd.read_csv('/tmp/{}.csv'.format(file_name))

    def initialize_expiry_fields(self):
        self.instrument_data.loc[:, 'tradingsymbol'] = self.instrument_data.instrument_symbol
        self.instrument_data.loc[:, 'expiry'] = pd.to_datetime(self.instrument_data.instrument_expiry)

        self.instrument_data.loc[:, "expiry_year"] = self.instrument_data["expiry"].dt.strftime("%y").astype(str)
        self.instrument_data.loc[:, "month"] = self.instrument_data["expiry"].dt.strftime("%b").str.upper()

        self.instrument_data.loc[:, "month_number"] = self.instrument_data["expiry"].dt.strftime("%m").astype(
            float).astype(str)
        self.instrument_data.loc[:, 'month_number'] = np.where(self.instrument_data.month_number == 'nan',
                                                               np.nan,
                                                               self.instrument_data.month_number.str.split(
                                                                   ".").str[0]
                                                               )

        self.instrument_data.loc[:, "week_option_prefix"] = np.where(
            self.instrument_data.month_number.astype(float) >= 10,
            self.instrument_data.month.str[0] + self.instrument_data["expiry"].dt.strftime("%d").astype(str),
            self.instrument_data.month_number + self.instrument_data["expiry"].dt.strftime("%d").astype(str),
        )

        self.instrument_data.loc[:, "next_expiry"] = self.instrument_data.expiry + pd.DateOffset(days=7)

    def execute_order_v2(self, order):
        start_time = datetime.now()
        tradingsymbol = order['tradingsymbol']
        exchange = order['exchange']
        trigger_price = order['trigger_price']
        transaction_type = order['transaction_type']
        if order['validity'] is not None and order['trigger_price'] is not None:
            while True:
                self.lock.acquire()
                try:
                    ltp = self.get_ltp(exchange, tradingsymbol)
                except Exception as e:
                    Constants.logger.error("[GET_LTP_FAILED] with exception {}".format(e))
                time.sleep(.5)
                self.lock.release()
                if (transaction_type == "SELL" and trigger_price > ltp) or (
                        transaction_type == "BUY" and trigger_price < ltp):
                    logger.info("[EXECUTING_ORDER] ltp {} crossed trigger price {} for {}".format(ltp, trigger_price, order))
                    self.execute_order(tradingsymbol=order['tradingsymbol'],
                                       exchange=order['exchange'],
                                       quantity=order['quantity'],
                                       product=order['product'],
                                       tag=order['tag'],
                                       stoploss=order['stoploss'],
                                       transaction_type=order['transaction_type'],
                                       order_type=order['order_type'])
                    return
                current_time = datetime.now()
                if (current_time - start_time).seconds > order['validity']:
                    Constants.logger.info("[ORDER_VALIDITY_EXPIRED] order [{}]".format(order))
                    return

    def execute_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                      stoploss=None, tag=None, product=None, price=None):
        upper_circuit = None
        if price is None:
            live_data = self.live_data(exchange=exchange, tradingsymbol=tradingsymbol)
            price = live_data['ltp']
            upper_circuit = live_data['upper_circuit']
            trade_price = copy.deepcopy(price)
        try:
            if stoploss != None:
                if transaction_type == "SELL":
                    sl_transaction_type = "BUY"
                    sl_trigger_price = self.round_to_tick(price * (1 + stoploss))

                    if exchange == self.nfo_exchange:
                        price = sl_trigger_price * 1.05
                    elif exchange == "NSE":
                        price = sl_trigger_price * 1.01
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                elif transaction_type == "BUY":
                    sl_transaction_type = "SELL"
                    sl_trigger_price = self.round_to_tick(price * (1 - stoploss))

                    if exchange == self.nfo_exchange:
                        price = sl_trigger_price * .95
                    elif exchange == "NSE":
                        price = sl_trigger_price * .99
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                else:
                    raise Exception("Invalid transaction_type {}".format(transaction_type))

                if upper_circuit != None and sl_price > upper_circuit:
                    raise Exception(f"[PRICE_BREACHED] {sl_price} is above upper circuit price [{upper_circuit}]")

                stoploss_order_id = self.place_order(tradingsymbol=tradingsymbol,
                                                     exchange=exchange,
                                                     quantity=quantity,
                                                     order_type=self.order_type_sl,
                                                     transaction_type=sl_transaction_type,
                                                     tag=tag, product=product, price=sl_price,
                                                     trigger_price=sl_trigger_price)

                if stoploss_order_id is None:
                    Constants.logger.error(
                        "[ORDER_REJECTED] tradingsymbol {}".format(tradingsymbol))
                    raise QuantplayOrderPlacementException("Order reject for {}".format(tradingsymbol))

            if order_type == "MARKET":
                trade_price = 0

            response = self.place_order(tradingsymbol=tradingsymbol, exchange=exchange, quantity=quantity,
                                        order_type=order_type, transaction_type=transaction_type, tag=tag,
                                        product=product, price=trade_price)
            return response
        except Exception as e:
            raise e

    """
            Input  : quantplay symbol
            Output : broker symbol
        """

    def get_symbol(self, symbol):
        return symbol

    """
        Input  : quantplay exchange
        Output : broker exchange
    """

    def get_order_type(self, order_type):
        return order_type

    def get_exchange(self, exchange):
        return exchange

    def live_data(self, exchange, tradingsymbol):
        return {
            'ltp' : self.get_ltp(exchange, tradingsymbol),
            'upper_circuit' : None,
            'lower_circuit' : None
        }
    def place_order_quantity(self, quantity, tradingsymbol, exchange):
        lot_size = self.get_lot_size(exchange, tradingsymbol)
        quantity_in_lots = int(quantity/lot_size)

        return quantity_in_lots*lot_size

    def get_product(self, product):
        return product

    def get_lot_size(self, exchange, tradingsymbol):
        try:
            return int(self.symbol_data["{}:{}".format(exchange, tradingsymbol)]['lot_size'])
        except Exception as e:
            logger.error("[GET_LOT_SIZE] unable to get lot size for {} {}".format(exchange, tradingsymbol))
            raise e

    def filter_orders(self, orders, tag=None, status=None):
        if tag:
            orders = orders[orders.tag == tag]

        if status:
            orders = orders[orders.status == status]

        return orders

    def option_symbol(self, underlying_symbol, expiry_date, strike_price, type):
        option_symbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[underlying_symbol]
        option_symbol += expiry_date.strftime('%y')

        month_number = str(int(expiry_date.strftime("%m")))
        monthly_option_prefix = expiry_date.strftime("%b").upper()

        if int(month_number) >= 10:
            week_option_prefix = monthly_option_prefix[0]
        else:
            week_option_prefix = month_number
        week_option_prefix += expiry_date.strftime("%d")

        next_expiry = expiry_date + timedelta(days=7)

        if next_expiry.month != expiry_date.month:
            option_symbol += monthly_option_prefix
        else:
            option_symbol += week_option_prefix

        option_symbol += str(int(strike_price))
        option_symbol += type

        return option_symbol


    def exit_all_trigger_orders(self, tag="ALL", symbol_contains=None):
        Constants.logger.error("exit all triggers implementation missing")
        pass

    def square_off_by_tag(self, tag, dry_run=True, sleep_time=0.05):
        self.exit_all_trigger_orders(tag=tag)
        orders = self.orders(tag=tag)

        if len(orders) == 0:
            logger.info(f"All positions with tag {tag} are already squared-off for {self.profile()}")
        orders.loc[:, 'exit_quantity'] = np.where(orders.transaction_type == "BUY",
                                                  -orders.filled_quantity,
                                                  orders.filled_quantity)
        exit_orders = orders.groupby('tradingsymbol').agg({'exit_quantity' : 'sum',
                                                           'exchange' : 'first',
                                                           'product' : 'first'
                                                           }).reset_index()

        orders_to_close = []
        exit_orders = exit_orders[exit_orders.exit_quantity != 0]
        positions = exit_orders.to_dict('records')
        for position in positions:
            exchange = position['exchange']
            tradingsymbol = position['tradingsymbol']
            quantity = position['exit_quantity']

            transaction_type = "SELL"
            if quantity == 0:
                continue
            elif quantity > 0:
                transaction_type = "BUY"

            quantity = abs(quantity)
            quantity_in_lots = int(quantity / self.get_lot_size(exchange, tradingsymbol))

            split_into = int(math.ceil(quantity_in_lots / 25))
            split_array = NumberUtils.split(abs(quantity_in_lots), abs(split_into))

            for q in split_array:
                orders_to_close.append(
                    {
                        'tradingsymbol': tradingsymbol,
                        'exchange': exchange,
                        'transaction_type': transaction_type,
                        'quantity_in_lots': q,
                        'product' : position['product']
                    })

        random.shuffle(orders_to_close)
        orders_to_close = sorted(orders_to_close, key=lambda d: d['transaction_type'])
        for order in orders_to_close:
            tradingsymbol = order['tradingsymbol']
            exchange = order['exchange']
            transaction_type = order['transaction_type']
            product = order['product']
            quantity = order['quantity_in_lots']*self.get_lot_size(exchange, tradingsymbol)
            quantity = self.place_order_quantity(quantity, tradingsymbol, exchange)

            print(tradingsymbol, exchange, transaction_type, quantity)
            if dry_run == False:
                self.place_order(tradingsymbol=tradingsymbol,
                                 exchange=exchange,
                                 quantity=quantity,
                                 order_type="MARKET",
                                 transaction_type=transaction_type,
                                 tag=tag,
                                 product=product,
                                 price=0)
                time.sleep(sleep_time)

        return orders_to_close


    def add_ltp(self, orders):
        orders.loc[:, 'exchange_symbol'] = orders.exchange + ":" + orders.tradingsymbol

        all_symbols = list(orders.exchange_symbol.unique())
        symbol_ltp = {}
        for exchange_symbol in all_symbols:
            ltp = self.get_ltp(exchange_symbol.split(":")[0], exchange_symbol.split(":")[1])
            symbol_ltp[exchange_symbol] = ltp
        orders.loc[:, 'ltp'] = orders['exchange_symbol'].map(symbol_ltp)

    def risk_analysis(self):
        positions = self.positions()
        positions.loc[:, 'net_quantity'] = positions.buy_quantity - positions.sell_quantity
        positions.loc[:, 'premium'] = positions.net_quantity*positions.ltp

        bank_nifty = positions[positions.tradingsymbol.str.contains("BANKNIFTY")]
        t_df = bank_nifty.groupby('option_type').premium.sum().reset_index()
        t_df.loc[:, 'segment'] = t_df.option_type
        t_df = t_df[['segment', 'premium']]
        response = {
            "banknifty_premium" : t_df
        }

        fin_nifty = positions[positions.tradingsymbol.str.contains("FINNIFTY")]
        t_df = fin_nifty.groupby('option_type').premium.sum().reset_index()
        t_df.loc[:, 'segment'] = t_df.option_type
        t_df = t_df[['segment', 'premium']]
        response["finnifty_premium"] = t_df

        return response
