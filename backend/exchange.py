import cbpro


class Exchange(object):
    def __init__(self, api_key=None, api_secret=None, password=None):
        if api_key and api_secret and password:
            self.client = cbpro.AuthenticatedClient(api_key, api_secret, password)
        else:
            self.client = cbpro.PublicClient()

    def get_historical_data(self, coin_pair, interval=3600):
        # Candlesticks need to be returned in reverse order (GDAX gives us most recent data first)
        print(interval)
        return self.client.get_product_historic_rates(coin_pair, granularity=interval)[::-1]

    def get_available_keypairs(self):
        return [product['display_name'] for product in self.client.get_products()]