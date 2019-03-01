from trade import Trade
import analysis
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

        print(buy_strategy)
        print(sell_strategy)

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


class BotStrategy(object):
    def __init__(self, coin_pair, buy_strategy, sell_strategy, stop_loss=None):

        self.pair = coin_pair
        self.buys = []
        self.sells = []
        self.indicators = BotStrategy.extract_indicators(buy_strategy) | BotStrategy.extract_indicators(sell_strategy)
        self.buy_strategy = buy_strategy
        self.sell_strategy = sell_strategy
        self.stop_loss = stop_loss

    @staticmethod
    def extract_indicators(strategy):
        """
        Extracts all of the indicators used in the given buy and sell strategies for this BotStrategy. Returns a set
        containing the JSON representation of each used indicator
        """

        if len(strategy) == 0:
            return set()

        # Expression evaluations
        if strategy['kind'] == 'And' or strategy['kind'] == 'Or':
            return BotStrategy.extract_indicators(strategy['e1']) | BotStrategy.extract_indicators(strategy['e2'])

        if strategy['kind'] == 'Not':
            return BotStrategy.extract_indicators(strategy['e'])

        indicators = set()

        left = strategy['l']
        right = strategy['r']

        # TODO(jbartola): Add support for other indicators (bollinger band, macd, etc.)
        if left['kind'] in {'sma', 'ema', 'rsi'}:
            indicators.add('{}-{}'.format(left['kind'], left['period']))

        if right['kind'] in {'sma', 'ema', 'rsi'}:
            indicators.add('{}-{}'.format(right['kind'], right['period']))

        return indicators

    def run(self, tohlcv_matrix, capital, trade):
        """
        Runs our strategy on a matrix of the most recent TOHLCV data

        Args:
            tohlcv_matrix (pandas.DataFrame): A dataframe containing TOHLCV + indicator data
            capital (float): The amount of capital left our reserve
        Returns:
            ('BUY' | 'SELL', capital) if a buy or sell was executed according to the provided strategies, otherwise
              returns None, None
        """
        import re

        # First, updated all the indicator values in-place in the tohlcv matrix
        for indicator in self.indicators:

            # Simple Moving Averages
            if re.fullmatch('sma-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                sma_df = analysis.analyze_sma(tohlcv_matrix, period)
                tohlcv_matrix[indicator] = sma_df[indicator]

            # Exponential Moving Averages
            if re.fullmatch('ema-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                ema_df = analysis.analyze_ema(tohlcv_matrix, period)
                tohlcv_matrix[indicator] = ema_df[indicator]

            # RSIs
            if re.fullmatch('rsi-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                rsi_df = analysis.analyze_sma(tohlcv_matrix, period)
                tohlcv_matrix[indicator] = rsi_df[indicator]

        lastrow = tohlcv_matrix.tail(1)
        current_price = lastrow['close'].item()
        current_time = lastrow.index.item() // 10**9

        indicator_datum = {ind : lastrow[ind].item() for ind in self.indicators}
        decision = Decision({'currentprice': current_price, **indicator_datum})

        if trade is None and decision.should_buy(self.buy_strategy):

            # Append the timestamp and the current price as a tuple
            self.buys.append((current_time, current_price))
            return Trade(self.pair, current_price, capital,
                         stop_loss=self.stop_loss), 'BUY'

        elif trade:
            if trade.can_sell() and (decision.should_sell(self.sell_strategy) or
                             (self.stop_loss and current_price < trade.stop_loss)):
                # Append the timestamp and the current price as a tuple
                self.sells.append((current_time, current_price))
                trade.close(current_price)
                return trade, 'SELL'

            elif trade


        return trade, None