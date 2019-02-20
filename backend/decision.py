
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

    def should_buy(self, buy_strategy):
        """
        Determines if we should buy given our buy strategies and our observed indicators

        Args:
            buy_strategy: A parsed Expression object containing the buy conditions for the given decision

        Returns:
            True iff each indicator satisfies a comparision using it's 'comparator' value with its 'value' value. False otherwise
        """

        if len(buy_strategy) == 0:
            return True

        # Expression evaluations
        if buy_strategy['kind'] == 'And':
            return self.should_buy(buy_strategy['e1']) and self.should_buy(buy_strategy['e2'])

        if buy_strategy['kind'] == 'Or':
            return self.should_buy(buy_strategy['e1']) or self.should_buy(buy_strategy['e2'])

        if buy_strategy['kind'] == 'Not':
            return not self.should_buy(buy_strategy['e'])

        # Indicator evaluations
        lv = self.get_indicator_value(buy_strategy['l'])
        rv = self.get_indicator_value(buy_strategy['r'])

        if lv is None or rv is None:
            return False

        if buy_strategy['kind'] == 'Eq':
            return lv == rv

        if buy_strategy['kind'] == 'LT':
            return lv < rv

        if buy_strategy['kind'] == 'LEq':
            return lv <= rv

        if buy_strategy['kind'] == 'GT':
            return lv > rv

        if buy_strategy['kind'] == 'GEQ':
            return lv >= rv

        return False

    def should_sell(self, sell_strategy):
        """
        Determines if we should sell given our sell strategies and our observed indicators

        Args:
            sell_strategy: A parsed Expression object containing the sell conditions for the given decision

        Returns:
             True iff each indicator satisfies a comparision using it's 'comparator' value with its 'value' value. False otherwise
        """

        if len(sell_strategy) == 0:
            return True

        # Expression evaluations
        if sell_strategy['kind'] == 'And':
            return self.should_buy(sell_strategy['e1']) and self.should_buy(sell_strategy['e2'])

        if sell_strategy['kind'] == 'Or':
            return self.should_buy(sell_strategy['e1']) or self.should_buy(sell_strategy['e2'])

        if sell_strategy['kind'] == 'Not':
            return not self.should_buy(sell_strategy['e'])

        # Indicator evaluations
        lv = self.get_indicator_value(sell_strategy['l'])
        rv = self.get_indicator_value(sell_strategy['r'])

        if lv is None or rv is None:
            return False

        if sell_strategy['kind'] == 'Eq':
            return lv == rv

        if sell_strategy['kind'] == 'LT':
            return lv < rv

        if sell_strategy['kind'] == 'LEq':
            return lv <= rv

        if sell_strategy['kind'] == 'GT':
            return lv > rv

        if sell_strategy['kind'] == 'GEQ':
            return lv >= rv

        return False
