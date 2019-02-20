
from exchange import Exchange
from analysis import *

def main(client, coin_pair, strategy, starting_capital, time_interval=900):

    hist_data = convert_to_dataframe(client.get_historical_data(coin_pair, interval=time_interval)).tail(100)

    while True:
        ticker_row = parse_ticker(client.get_ticker(coin_pair))

        # Pad the row with NaNs so we can add it to the historical dataframe
        ticker_row.extend([float('nan') for _ in range(len(hist_data.columns) - len(ticker_row))])
        hist_data.loc[len(hist_data)] = ticker_row
        hist_data = hist_data.iloc[1:]

        strategy.run(hist_data)




        # Example ticker: {'trade_id': 45061543, 'price': '144.49000000', 'size': '0.25000000', 'time': '2019-02-18T23:15:21.909Z', 'bid': '144.5', 'ask': '144.51', 'volume': '329857.10844567'}


def parse_ticker(ticker):
    """
    Parses a ticker object and returns a row containing TOHLCV data
    Args:
        ticker (dict): A dictionary mapping TOHLCV data to their values
    Returns:
        list[float]: A list denoting one entry for each column of a TOHLCV dataframe
    """
    from datetime import datetime
    date = datetime.strptime(ticker['time'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Mark the high as the ask, low as the bid, and close as the curent price.
    return [date, float(ticker['ask']), float(ticker['bid']), float(ticker['price']), float(ticker['volume'])]


def climain():
from exchange import Exchange
from analysis import *

client = Exchange(api_key="3cfdad137dc42d0478fd75074c07839e",
                  api_secret="ff273wPasA7PUMyO/cm9Wbs0uNOYYbj3885bTvAHvrkeVDflcCCXpWDccYT3jBg0mn0wGvW++WbixawHPmUL9Q==",
                  password="ib4yucdr5w")
hd = client.get_historical_data('ETH-USD')





if __name__ == "__main__":
    pass