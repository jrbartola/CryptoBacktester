import pandas as pd
import numpy as np

from exchange import Exchange
from analysis import *


def main(client, coin_pair, buy_strategy, sell_strategy, starting_capital, time_interval=900):
    import time

    open_order = False
    capital = starting_capital
    strategy = BotStrategy(coin_pair, buy_strategy, sell_strategy)

    hist_data = convert_to_dataframe(client.get_historical_data(coin_pair, interval=time_interval)).tail(100)
    print("Historical data acquired.")

    while True:
        ticker_row = parse_ticker(client.get_ticker(coin_pair))
        timestamp = ticker_row.pop('datetime')

        ticker_series = pd.Series(ticker_row, name=timestamp)

        hist_data = hist_data.append(ticker_series)
        hist_data = hist_data.iloc[1:]
        last_row = hist_data.tail(1)

        print("({}): {}".format(timestamp, last_row['close'].item()))

        # Check the open order to see if we can run the strategy yet. If not, skip the strategy and wait again
        if not open_order:
            trade_type, remaining_capital = strategy.run(hist_data, capital)
            capital = remaining_capital or capital

        # Sleep for `time_interval` number of seconds
        time.sleep(10)



def parse_ticker(ticker):
    """
    Parses a ticker object and returns a row containing TOHLCV data
    Args:
        ticker (dict): A dictionary mapping TOHLCV data to their values
    Returns:
        dict[str, -]: A dictionary denoting one entry for each column of a TOHLCV dataframe
    """
    from datetime import datetime
    date = datetime.strptime(ticker['time'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Mark the high as the ask, low as the bid, and close as the current price. Open is 0
    return {'datetime': np.array([date]).astype('datetime64[s]')[0],
            'open': 0,
            'high': float(ticker['ask']),
            'low': float(ticker['bid']),
            'close': float(ticker['price']),
            'volume': float(ticker['volume'])}




if __name__ == "__main__":
from exchange import Exchange
from strategy import BotStrategy

client = Exchange(api_key="9ddbca41212574bbe9deb9f87398f3b3",
              api_secret="0EB8xMFulM+xpGkiFJGM8zxzn40FlLMR9acdfIBASa67C0Jqpj7J3OKpLJiToHe5S859vNSGsI5/ha9SdTaNCw==",
              password="36m26w6v48d")
buy_strategy = {'l': {'kind': 'currentprice'}, 'r': {'period': '9', 'kind': 'sma'}, 'kind': 'GT'}
sell_strategy = {'l': {'kind': 'currentprice'}, 'r': {'period': '9', 'kind': 'sma'}, 'kind': 'LT'}


    main(client, 'ETH-USD', buy_strategy=buy_strategy,
         sell_strategy=sell_strategy, starting_capital=1000, time_interval=60)
