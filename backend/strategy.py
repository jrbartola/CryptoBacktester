from trade import Trade
from analysis import *
from decision import Decision


class BacktestingStrategy(object):
    def __init__(self, pair, capital, buy_strategy, sell_strategy, trading_fee=0, stop_loss=0):
        self.trade = None
        self.sells = []
        self.buys = []
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
        prices = [[candle.time, 0, 0, 0, candle.close, 0] for candle in candlesticks]

        for i in range(len(prices)):

            # Get the (sampled) closing price
            current_price = prices[i][4]
            current_time = prices[i][0]

            # Each indicator data point is a 2-tuple containing (timestamp, value)
            indicator_datum = {ind : indicators[ind][i][1] for ind in indicators}
            decision = Decision({'currentprice': current_price, **indicator_datum})

            ### CHECK TO SEE IF WE CAN OPEN A BUY POSITION
            if self.trade is None and decision.should_buy(self.buy_strategy):
                assert self.reserve > 0

                self.buys.append((current_time, current_price))
                new_trade = Trade(self.pair, current_price, self.reserve * (1 - self.trading_fee),
                                  stop_loss=self.stop_loss)
                self.reserve = 0
                self.trade = new_trade

            ### CHECK TO SEE IF WE NEED TO SELL ANY OPEN POSITIONS OR HIT A STOP LOSS
            elif self.trade and (decision.should_sell(self.sell_stategy) or
                               self.trade.stop_loss and current_price < self.trade.stop_loss):

                profit, total = self.trade.close(current_price)
                self.sells.append((current_time, current_price))
                self.profit += profit * (1 - self.trading_fee)
                self.reserve = total * (1 - self.trading_fee)
                self.trade = None

    def show_positions(self):
        if self.trade:
            self.trade.show_trade()


class BotStrategy(object):
    def __init__(self, indicators, buy_strategy, sell_strategy, stop_loss=None):

        self.buys = []
        self.sells = []
        self.indicators = indicators
        self.buy_strategy = buy_strategy
        self.sell_strategy = sell_strategy
        self.stop_loss = stop_loss
        self.trade = None

    def run(self, tohlcv_matrix):
        """
        Runs our strategy on a matrix of the most recent TOHLCV data

        Args:
            tohlcv_matrix (pandas.DataFrame): A dataframe containing TOHLCV + indicator data
        """
        import re

        indicator_values = {}

        # First, updated all the indicator values in-place in the tohlcv matrix
        for indicator in self.indicators:

            # Simple Moving Averages
            if re.fullmatch('sma-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                sma_df = analysis.analyze_sma(tohlcv_matrix, period)
                tohlcv_matrix[indicator] = sma_df[[indicator]]

            # Exponential Moving Averages
            if re.fullmatch('ema-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                ema_df = analysis.analyze_ema(tohlcv_matrix, period)
                tohlcv_matrix[indicator] = ema_df[[indicator]]

            # RSIs
            if re.fullmatch('rsi-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                rsi_df = analysis.analyze_sma(tohlcv_matrix, period)
                tohlcv_matrix[indicator] = rsi_df[[indicator]]


        lastrow = tohlcv_matrix.tail(1)
        current_price = lastrow['close'].item()

        indicator_datum = {ind : lastrow[ind].item() for ind in self.indicators}
        decision = Decision({'currentprice': current_price, **indicator_datum})

        if self.trade is None and decision.should_buy(self.buy_strategy):

            # Append the timestamp and the current price as a tuple
            self.buys.append((lastrow.index.item() // 10**9, current_price))
            new_trade = Trade(self.pair, current_price, self.reserve * (1 - self.trading_fee),
                              stop_loss=self.stop_loss)
            self.trade = new_trade

        else:

            if decision.should_sell(self.sell_strategy) or (self.stop_loss and current_price < self.trade.stop_loss):
                self.sells.append((current_time, current_price))
                profit, total = trade.close(current_price)
                self.profit += profit * (1 - self.trading_fee)
                self.reserve = total * (1 - self.trading_fee)


    def show_positions(self):
        for trade in self.trades:
            trade.show_trade()