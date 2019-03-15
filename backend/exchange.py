import cbpro

from analysis import convert_to_dataframe


class Exchange(object):
    def __init__(self, api_key=None, api_secret=None, password=None):
        if api_key and api_secret and password:
            self.client = cbpro.AuthenticatedClient(api_key, api_secret, password)
        else:
            self.client = cbpro.PublicClient()

    def get_historical_data(self, coin_pair, interval=3600):
        """
        Retrieve the historical data for a given coin pair over the specified time interval
        Args:
            coin_pair (str): The coin pair to fetch data for
            interval (int): The interval of time (in seconds) between successive datapoints
        Returns:
            pandas.DataFrame: A dataframe containing the corresponding OHLCV data
        """

        # Candlesticks need to be returned in reverse order (GDAX gives us most recent data first)
        return convert_to_dataframe(
            self.client.get_product_historic_rates(coin_pair, granularity=interval)[::-1]
        )

    def get_available_keypairs(self):
        return [product['display_name'] for product in self.client.get_products()]

    def get_ticker(self, coin_pair):
        return self.client.get_product_ticker(coin_pair)

    def buy(self, coin_pair, amount, limit=None):
        """
        Buys the specified coin pair at the given price per coin. In total will spend price * amount of
        the quote currency
        Args:
            coin_pair (str): The base-quote currency pair that will be traded
            amount (float): The amount of the base currency to purchase
            limit (float): The amount of the base currency that is to be purchased. Defaults to None if this
              is executed as a market order
        """

        if limit:
            return self.client.place_limit_order(side='buy', product_id=coin_pair, price=limit, size=amount)

        return self.client.place_market_order(side='buy', product_id=coin_pair, size=amount)

    def sell(self, coin_pair, amount, limit=None):
        """
        Sells the specified coin pair at the given price per coin. In total gain spend price * amount of
        the base currency
        Args:
            coin_pair (str): The base-quote currency pair that will be traded
            amount (float): The amount of the base currency to sell
            limit (float): The amount of the base currency that is to be sold. Defaults to None if this
              is executed as a market order
        """

        if limit:
            return self.client.place_limit_order(side='sell', product_id=coin_pair, price=limit, size=amount)

        return self.client.place_market_order(side='sell', product_id=coin_pair, size=amount)

    def get_order(self, uuid):
        return self.client.get_order(uuid)