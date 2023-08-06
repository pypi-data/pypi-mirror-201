from quantplay.indicators.atr import ATR

class Indicator:
    def __init__(self):
        pass

    @staticmethod
    def ema(series, periods, fillna=False):
        if fillna:
            return series.ewm(span=periods, min_periods=0).mean()

        return series.ewm(span=periods, min_periods=periods).mean()


    @staticmethod
    def atr(high, low, close, timeperiod=14):
        return ATR.get_value(high, low, close, timeperiod=timeperiod)