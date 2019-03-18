import analysis
from trade import Trade
from decision import Decision
from util import epoch_to_str


class Chart(object):
    """
    A Chart class encompassing functionality for a set of historical data in a time-series domain. Contains functionality
    for backtesting various strategies over historical data
    """
    def __init__(self, coin_pair, ohlcv_matrix, indicators):

        self.pair = coin_pair
        self.data = ohlcv_matrix

        # Append the indicators to our OHLCV matrix
        self.__add_indicators(indicators)

    def get_data(self, start_time=None):
        """
        Retrieve all OHLCV data from the chart. If a start time is specified, then we return data only
        from that time onward. By default we return all data

        Args:
            start_time (int): Defaults to None. Otherwise is an integer denoting the starting time in epoch seconds
                that our candles will be returned from
        Returns:
            list[Candlestick]: A list of candlestick objects
        """
        if start_time:
            return self.data.loc[epoch_to_str(start_time):]

        return self.data

    def __add_indicators(self, indicators):
        """
        Updates the OHLCV dataframe with the indicators specified in the input list

        Args:
            indicators (list[str]): A list of strings where each string is a JSON representation of an indicator
        """
        import re

        for indicator in indicators:

            # Simple Moving Averages
            if re.fullmatch('sma-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])
                self.data = analysis.analyze_sma(self.data, period_count=period)

            # Exponential Moving Averages
            if re.fullmatch('ema-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])
                self.data = analysis.analyze_ema(self.data, period_count=period)

            # RSIs
            if re.fullmatch('rsi-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])
                self.data = analysis.analyze_rsi(self.data, period_count=period)

            # Bollinger Bands
            if re.fullmatch('bollinger-\d+-\d+', indicator):
                period, std_dev = [int(m) for m in re.findall('\d+', indicator)]

                self.data = analysis.analyze_bollinger_bands(self.data, period_count=period)

        self.data = self.data.where(self.data.notnull(), None)

    def run_backtest(self, capital, buy_strategy, sell_strategy, trading_fee=0, stop_loss=0):
        """
        Runs our backtesting strategy on the set of candlestick data

        Args:
            self.data (pandas.DataFrame): A dataframe consisting of OHLCV + indicator data
            capital (float): The starting capital of the quote currency
            buy_strategy (dict[-, -]): A dictionary containing a buy strategy as specified by the parser documentation
            sell_strategy (dict[-, -]): A dictionary containing a sell strategy as specified by the parser documentation
            trading_fee (float | 0): The trading fee per market order. Defaults to 0
            stop_loss (float | 0): The amount of quote currency below our buy point at which to sell an open position
        Returns:
            dict[str, -]: A dictionary mapping data to a dictionary representation of the dataframe and the profit to the
              resulting profit from the backtest
        """

        reserve = capital
        trade: Trade = None

        # First append a buy, sell and profit column to our dataframe (with default value False)
        self.data.insert(len(self.data.columns), 'buy', False)
        self.data.insert(len(self.data.columns), 'sell', False)

        # Add the profit column (with default value 0)
        self.data.insert(len(self.data.columns), 'profit', 0)

        # Run our strategy on each data point in the matrix
        for date_index, row in self.data.iterrows():

            current_price = row['close']

            # All the indicator fields are placed after the 5 columns of OHLCV (and before buy, sell, profit) data
            indicator_datum = {ind: row[ind] for ind in row.index[5:-3]}
            decision = Decision({'currentprice': current_price, **indicator_datum})

            # Check to see if we can open a position
            if not trade and decision.should_execute(buy_strategy):
                self.data.loc[date_index, 'buy'] = True
                trade = Trade(self.pair, current_price, reserve * (1 - trading_fee))
                reserve = 0

            # Check to see if we can sell our position or if we hit a stop loss
            elif trade:

                profit = current_price * trade.amount_base - capital
                self.data.loc[date_index, 'profit'] = profit

                if decision.should_execute(sell_strategy) or (stop_loss and current_price < trade.entry_price * (1 - stop_loss)):
                    self.data.loc[date_index, 'sell'] = True
                    reserve = current_price * trade.amount_base * (1 - trading_fee)
                    trade.close(current_price)
                    trade = None
