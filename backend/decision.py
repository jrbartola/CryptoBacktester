
"""
Decision encapsulates a boolean process that determines when to open and close a trade
"""
class Decision(object):
    def __init__(self, indicators):
        self.indicators = indicators

    def get_indicator_value(self, indicator):
        if indicator['kind'] == 'real':
            return float(indicator['val'])
        if indicator['kind'] == 'currentprice':
            return self.indicators['currentprice']

        # TODO(jbartola): Add support for bollinger bands and macd
        return self.indicators['{}-{}'.format(indicator['kind'], indicator['period'])]

    def should_execute(self, strategy):
        """
        Determines if we should execute a given strategy based on our observed indicators

        Args:
            strategy: A parsed Expression object containing the conditions for a buy/sell strategy

        Returns:
            True iff each indicator satisfies a comparision using it's 'comparator' value with its 'value' value. False otherwise
        """

        if len(strategy) == 0:
            return True

        # Expression evaluations
        if strategy['kind'] == 'And':
            return self.should_execute(strategy['e1']) and self.should_execute(strategy['e2'])

        if strategy['kind'] == 'Or':
            return self.should_execute(strategy['e1']) or self.should_execute(strategy['e2'])

        if strategy['kind'] == 'Not':
            return not self.should_execute(strategy['e'])

        # Indicator evaluations
        lv = self.get_indicator_value(strategy['l'])
        rv = self.get_indicator_value(strategy['r'])

        if lv is None or rv is None:
            return False

        if strategy['kind'] == 'Eq':
            return lv == rv

        if strategy['kind'] == 'LT':
            return lv < rv

        if strategy['kind'] == 'LEq':
            return lv <= rv

        if strategy['kind'] == 'GT':
            return lv > rv

        if strategy['kind'] == 'GEQ':
            return lv >= rv

        return False
