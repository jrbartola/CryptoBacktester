
from chart import Chart
from strategy import BacktestingStrategy

"""
A Backtesting engine
"""
class Backtester(object):
    def __init__(self, coin_pair, period_length, exchange_interface, capital, stop_loss,
                 buy_strategy, sell_strategy, start_time=None, indicators=[]):

        self.start_time = start_time
        self.chart = Chart(coin_pair, period_length, exchange_interface)
        self.strategy = BacktestingStrategy(pair=coin_pair, capital=capital, buy_strategy=buy_strategy,
                                            sell_strategy=sell_strategy, trading_fee=0.0025, stop_loss=stop_loss)
        self.indicators = self.chart.get_indicators(indicators, start_time)

    def run(self):
        """
        Run our backtesting strategy on the set of historical data parsed as candlesticks
        """
        candlesticks = self.chart.get_points(self.start_time)
        self.strategy.run(candlesticks, self.indicators)

    def get_results(self):
        """
        Return the results of our backtesting execution

        Returns:
            dict[str, -]: A dictionary mapping strings to their result properties
        """
        closings = [[d.time, d.close] for d in self.chart.get_points(self.start_time)]

        results = {'buys': list(self.strategy.buys), 'sells': list(self.strategy.sells), 'closingPrices': closings,
                   'indicators': self.indicators, 'profit': round(self.strategy.profit, 8)}

        return results
