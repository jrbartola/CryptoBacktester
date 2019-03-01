
class Trade(object):
    def __init__(self, pair, current_price, amt_btc, uuid=None, stop_loss=None, client=None):
        self.status = 'open-unfilled'
        self.pair = pair
        self.entry_price = current_price
        self.exit_price = None
        self.profit = 0
        self.end_quote = 0
        self.amount = amt_btc / current_price
        self.client = client
        self.uuid = uuid

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

    def __print_buy_msg(self):
        print("Opened {} trade at {}. Spent: {} {}, Amount: {} {}".format(self.pair,
                                                                          self.entry_price,
                                                                          round(self.amount * self.entry_price, 8),
                                                                          self.pair[4:],
                                                                          round(self.amount, 8),
                                                                          self.pair.split('-')[0]))

    def __print_sell_msg(self):
        message_type = "\033[92m" if self.profit >= 0 else "\033[91m"

        print(message_type + "Sold {} at {}. Profit: {}, Total {}: {} \033[0m".format(self.pair[:3],
                                                                                  self.exit_price,
                                                                                  round(self.profit, 8),
                                                                                  self.pair[4:],
                                                                                  round(self.amount * self.exit_price, 8)))

    def tick(self):
        """
        Checks the CoinbasePro API to see if an open order has been filled
        Returns:
            The status of the current order.
        """
        # Only perform a tick check if we are live trading
        if self.client is None:
            return None

        if self.status == 'open-unfilled':
            if self.client.get_order(self.uuid)['status'] == 'done':
                self.__print_buy_msg()
                self.status = 'open'
        if self.status == 'closed-unfilled':
            if self.client.get_order(self.uuid)['status'] == 'done':
                self.__print_sell_msg()
                self.status = 'closed'

        return self.status

    def can_sell(self):
        return self.status == 'open'

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

        # SELL RESPONSE SAMPLE: {'id': '6ad607f2-8a21-4467-90ed-e21d3b46a449', 'price': '1000.00000000', 'size': '0.01000000', 'product_id': 'BTC-USD', 'side': 'sell', 'stp': 'dc', 'type': 'limit', 'time_in_force': 'GTC', 'post_only': False, 'created_at': '2019-02-26T05:58:18.758725Z', 'fill_fees': '0.0000000000000000', 'filled_size': '0.00000000', 'executed_value': '0.0000000000000000', 'status': 'pending', 'settled': False}

        return self.profit, btc_ended
