
"""
A candlestick object, part of a time-series chart of historical data
"""
class Candlestick(object):
    def __init__(self, time=None, open=None, close=None, high=None, low=None, price_average=None):
        self.current = None
        self.time = time
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.price_average = price_average


