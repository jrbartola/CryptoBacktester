import logger


class Trade(object):
    """
    The Trade class encompasses a trade performed during a backtesting operation

    Args:
        pair (str): The coin pair that is being traded
        current_price (float): The current price for one unit of the base currency
        amount_quote (float): The amount of quote currency being purchased
    """
    def __init__(self, pair, current_price, amount_quote):
        self.pair = pair
        self.entry_price = current_price
        self.exit_price = None
        self.amount_base = round(amount_quote / current_price, 8)

        logger.log("Opened {} trade at {}. Spent: {} {}, Amount: {} {}".format(pair,
                                                                               self.entry_price,
                                                                               round(amount_quote, 8),
                                                                               self.pair[4:],
                                                                               self.amount_base,
                                                                               pair.split('-')[0]))

    def close(self, current_price):
        self.exit_price = current_price

        btc_started = self.amount_base * self.entry_price
        btc_ended = self.amount_base * self.exit_price
        profit = btc_ended - btc_started

        message_type = "success" if profit > 0 else "error"
        logger.log("Sold {} at {}. Profit: {}, Total {}: {}".format(self.pair[:3],
                                                                                   self.exit_price,
                                                                                   round(profit, 8),
                                                                                   self.pair[4:],
                                                                                   round(btc_ended, 8)), type=message_type)

