import random

from trade import Trade
from analysis import StrategyAnalyzer
from decision import Decision


class BacktestingStrategy(object):
    def __init__(self, pair, capital, buy_strategy, sell_strategy, trading_fee=0, stop_loss=0):
        self.prices = []
        self.trades = []
        self.sells = []
        self.buys = []
        self.max_trades_at_once = 1
        self.indicators = StrategyAnalyzer()
        self.profit = 0
        self.pair = pair
        self.reserve = capital
        self.buy_strategy = buy_strategy
        self.sell_stategy = sell_strategy
        self.trading_fee = trading_fee
        self.stop_loss = stop_loss

    def run(self, candlesticks, indicators):
        """
        Runs our backtesting strategy on the set of candlestick data

        Args:
            candlesticks (list[Candlestick]): A list of candlestick objects
            indicators (dict[str, -]): A dictionary mapping indicator strings to their data points
        """

        # The zero's are to take up space since our indicators require a full dataframe of OHLC datas
        self.prices = [[candle.time, 0, 0, 0, candle.close, 0] for candle in candlesticks]

        for i in range(len(self.prices)):

            # Get the (sampled) closing price
            current_price = self.prices[i][4]
            current_time = self.prices[i][0]

            indicator_datum = {ind : indicators[ind][i][1] for ind in indicators}
            decision = Decision({'currentprice': current_price, **indicator_datum})

            open_trades = [trade for trade in self.trades if trade.status == 'OPEN']

            ### CHECK TO SEE IF WE CAN OPEN A BUY POSITION
            if len(open_trades) < self.max_trades_at_once:
                if decision.should_buy(self.buy_strategy):
                    assert self.reserve > 0

                    self.buys.append((current_time, current_price))
                    new_trade = Trade(self.pair, current_price, self.reserve * (1 - self.trading_fee),
                                      stop_loss=self.stop_loss)
                    self.reserve = 0
                    self.trades.append(new_trade)

            ### CHECK TO SEE IF WE NEED TO SELL ANY OPEN POSITIONS
            for trade in open_trades:
                if decision.should_sell(self.sell_stategy):

                    self.sells.append((current_time, current_price))
                    profit, total = trade.close(current_price)
                    self.profit += profit * (1 - self.trading_fee)
                    self.reserve = total * (1 - self.trading_fee)

            ### CHECK TO SEE IF WE HAVE ACTIVATED A STOP LOSS
            for trade in self.trades:

                # Check our stop losses
                if trade.status == "OPEN" and trade.stop_loss and current_price < trade.stop_loss:
                    profit, total = trade.close(current_price)
                    self.sells.append((current_time, current_price))
                    self.profit += profit * (1 - self.trading_fee)
                    self.reserve = total * (1 - self.trading_fee)

    def show_positions(self):
        for trade in self.trades:
            trade.show_trade()
