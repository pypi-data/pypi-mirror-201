import numpy as np
import plotly.graph_objects as go
import pandas as pd



class TradeLens:

    @staticmethod
    def plot(dataset, interval, symbol):
        symbol = "BANKNIFTY2111432100PE"
        df = pd.read_csv(f"~/.quantplay/{dataset}/{interval}/{symbol}.csv")

        fig = go.Figure(data=go.Ohlc(x=df['date'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']))
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.show()
    @staticmethod
    def max_drawdowns(trades):
        trades = trades.sort_values("order_timestamp")
        temp_df = trades[['order_timestamp', 'profit']]

        for j in range(0, 5):
            temp_df.loc[:, 'balance'] = temp_df.profit.cumsum()
            temp_df.loc[:, 'running_max_balance'] = np.maximum.accumulate(temp_df.balance)
            temp_df.loc[:, 'drawdowns'] = temp_df.running_max_balance - temp_df.balance

            max_drawdown = np.max(temp_df.drawdowns)
            end_index = None
            for i in range(0, len(temp_df)):
                end_index = len(temp_df) - 1 - i
                if temp_df.iloc[end_index]['drawdowns'] != max_drawdown:
                    continue

                start_index = end_index
                while temp_df.iloc[start_index - 1]['running_max_balance'] == temp_df.iloc[start_index]['running_max_balance']:
                    start_index = start_index - 1

                print("Max drawdown {} from {} till {} amount {}".format(j,
                                                               temp_df.iloc[start_index]['order_timestamp'],
                                                               temp_df.iloc[end_index]['order_timestamp'],
                                                                        max_drawdown))

                temp_df = temp_df.drop(temp_df.index[start_index:end_index])
                break


    @staticmethod
    def analyse(trades, disable_metrics=[]):
        exchanges = list(trades.exchange.unique())
        trades.loc[:, 'segment'] = np.where("PE" == trades.tradingsymbol.str[-2:], "PE", "CE")

        trades.loc[:, 'hour'] = trades.date.dt.hour
        trades.loc[:, "day_of_week"] = trades.date.dt.day_name()

        if "hour" not in disable_metrics:
            print(trades.groupby('hour').profit.mean())

        if "day_of_week" not in disable_metrics:
            print(trades.groupby('day_of_week').profit.mean())

        if "hour:day_of_week" not in disable_metrics:
            print(trades.groupby(['hour', 'day_of_week']).profit.mean())

        if len(exchanges) == 1 and exchanges[0] == "NFO":
            if "segment" not in disable_metrics:
                print(trades.groupby('segment').profit.mean())
            if "segment:day_of_week" not in disable_metrics:
                print(trades.groupby(['segment', 'day_of_week']).profit.mean())
            if "hour:segment" not in disable_metrics:
                print(trades.groupby(['hour', 'segment']).profit.mean())

        trades.loc[:, 'trade_return'] = trades.profit / trades.exposure
        trades.loc[:, 'time'] = trades.order_timestamp.dt.time.astype(str)

        if "time" not in disable_metrics:
            print("Trade return by time")
            print(trades.groupby('time').trade_return.mean())

        trades.loc[:, 'trade_return'] = trades.close_price / trades.entry_price - 1
        print("Mean return of trades")
        print(trades.trade_return.mean())

        trades.loc[:, 'week_number'] = (trades.order_timestamp.dt.day / 7).astype(int)
        if "week_number" not in disable_metrics:
            print("profit by week number")
            print(trades.groupby('week_number').profit.mean())

