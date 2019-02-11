from analysis import StrategyAnalyzer
from candlestick import Candlestick

"""
A Chart class encompassing functionality for a set of historical data in a time-series domain
"""
class Chart(object):
    def __init__(self, pair, period, exchange_interface):

        self.pair = pair
        self.indicators = StrategyAnalyzer()
        self.data = []

        # Query the data to fill our chart truncate it to 'length' elements
        raw_data = exchange_interface.get_historical_data(pair, interval=Chart.period_to_integer(period))

        for datum in raw_data:
            stick = Candlestick(time=datum[0],
                                open=datum[1],
                                high=datum[2],
                                low=datum[3],
                                close=datum[4],
                                price_average=(datum[2] + datum[3])/2.)
            self.data.append(stick)

    def get_points(self, start_time=None):
        """
        Retrieve all candlesticks from the chart. If a start time is specified, then we return candlesticks only
        from that time onward. By default we return all candlesticks

        Args:
            start_time (int): Defaults to None. Otherwise is an integer denoting the starting time in epoch seconds
                that our candles will be returned from

        Returns:
            list[Candlestick]: A list of candlestick objects
        """
        if start_time:
            return [stick for stick in self.data if stick.time >= start_time]

        return self.data

    @staticmethod
    def period_to_integer(period):
        """
        Converts a period string into a integer
        Args:
            period (str): A string denoting the period of time each candlestick represents (i.e., '15m')
        Returns:
            int: An integer denoting the period of time in seconds
        """

        import re

        try:
            num_units = re.findall(r'\d+', period)[0]
            unit_type = period[len(num_units):]
            if unit_type == 'm':
                return 60 * int(num_units)
            if unit_type == 'h':
                return 60 * 60 * int(num_units)
            if unit_type == 'd':
                return 24 * 60 * 60 * int(num_units)

        except IndexError:
            raise ValueError("`Period` string should contain a character prefixed with an integer")

    def get_indicators(self, indicators, start_time):
        """
        Returns the indicators specified in the input list as a json-serializable dictionary

        Args:
            indicators (list[str]): A list of strings where each string is a JSON representation of an indicator
            start_time (int): The earliest data point to consider, in epoch milliseconds
        Returns:
            dict[str, -]: A response dictionary mapping JSON indicator names to their data points
        """
        import re

        start_time = start_time if start_time else 0
        response = {}

        # Get closing historical datapoints
        closings = [[x.time, 0, 0, 0, x.close, 0] for x in self.get_points(start_time)]

        for indicator in indicators:

            # Simple Moving Averages
            if re.fullmatch('sma-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                response[indicator] = [(closings[i][0], None) for i in range(period)] + \
                                      [(closings[i + period-1][0], datum["values"][0]) for i, datum in
                                       enumerate(self.indicators.analyze_sma(closings, period_count=period, all_data=True))]

            # RSIs
            if re.fullmatch('rsi-\d+', indicator):
                period = int(indicator[indicator.find('-') + 1:])

                response[indicator] = [(closings[i][0], None) for i in range(period)] + \
                                      [(closings[i + period - 1][0], datum["values"][0]) for i, datum in
                                       enumerate(self.indicators.analyze_rsi(closings, period_count=period, all_data=True))]

            # Bollinger Bands
            if re.fullmatch('bollinger-\d+-\d+', indicator):
                period, std_dev = [int(m) for m in re.findall('\d+', indicator)]

                # Offset each band by "period" data points
                bbupper = [(closings[i + period-1][0], datum["values"][0]) for i, datum in
                           enumerate(self.indicators.analyze_bollinger_bands(closings, all_data=True))]
                bblower = [(closings[i + period-1][0], datum["values"][2]) for i, datum in
                           enumerate(self.indicators.analyze_bollinger_bands(closings, all_data=True))]

                response['bollinger_upper'] = bbupper
                response['bollinger_lower'] = bblower

        return response
