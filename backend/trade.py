import logger

class Trade(object):
    def __init__(self, pair, current_price, amt_btc, uuid=None, stop_loss=None, client=None):
        self.status = 'open-unfilled'
        self.pair = pair
        self.entry_price = current_price
        self.exit_price = None
        self.amount = round(amt_btc / current_price, 8)
        self.client = client
        self.uuid = uuid
        self.profit = 0

        if stop_loss:
            self.stop_loss = current_price * (1 - stop_loss)
        else:
            self.stop_loss = None

        if self.client:
            resp = client.buy(self.pair, self.amount, limit=self.entry_price)

            # If there was a message from the buy request, then the order couldn't be completed for some reason
            if 'message' in resp:
                raise RuntimeError(resp['message'])

            self.uuid = resp['id']

        logger.log("Opened {} trade at {}. Spent: {} {}, Amount: {} {}".format(pair,
                                                                          self.entry_price,
                                                                          round(amt_btc, 8),
                                                                          self.pair[4:],
                                                                          self.amount,
                                                                          pair.split('-')[0]))

    def order_is_open(self):
        """
        Checks the CoinbasePro API to see if an open order has been filled
        Returns:
            True if the order is still open, False if it has been filled
        """
        # Only perform a tick check if we are live trading
        if self.client is None:
            return False

        if self.status == 'open-unfilled' and self.client.get_order(self.uuid)['status'] == 'done':
            self.status = 'open'
            logger.log("Open buy order was filled.")
        if self.status == 'closed-unfilled' and self.client.get_order(self.uuid)['status'] == 'done':
            self.status = 'closed'
            logger.log("Open sell order was filled.")

        return self.status != 'open' and self.status != 'closed'

    def close(self, current_price):
        if self.client:
            resp = self.client.sell(self.pair, self.amount, limit=current_price)

            # If there was a message from the sell request, then the order couldn't be completed for some reason
            if 'message' in resp:
                raise RuntimeError(resp['message'])

            self.uuid = resp['id']
            self.status = "closed-unfilled"

        self.exit_price = current_price

        btc_started = self.amount * self.entry_price
        btc_ended = self.amount * self.exit_price
        self.profit = btc_ended - btc_started

        message_type = "success" if self.profit > 0 else "error"

        logger.log(message_type + "Sold {} at {}. Profit: {}, Total {}: {}".format(self.pair[:3],
                                                                                      self.exit_price,
                                                                                      round(self.profit, 8),
                                                                                      self.pair[4:],
                                                                                      round(btc_ended, 8)))

        # SELL RESPONSE SAMPLE: {'id': '6ad607f2-8a21-4467-90ed-e21d3b46a449', 'price': '1000.00000000', 'size': '0.01000000', 'product_id': 'BTC-USD', 'side': 'sell', 'stp': 'dc', 'type': 'limit', 'time_in_force': 'GTC', 'post_only': False, 'created_at': '2019-02-26T05:58:18.758725Z', 'fill_fees': '0.0000000000000000', 'filled_size': '0.00000000', 'executed_value': '0.0000000000000000', 'status': 'pending', 'settled': False}

        return profit, btc_ended
