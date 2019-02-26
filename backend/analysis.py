"""Executes the trading strategies and analyzes the results.
"""

import math
from datetime import datetime

import pandas
from talib import abstract


def convert_to_dataframe(historical_data):
    """Converts historical data matrix to a pandas dataframe.

    Args:
        historical_data (list): A matrix of historical OHCLV data.

    Returns:
        pandas.DataFrame: Contains the historical data in a pandas dataframe.
    """

    dataframe = pandas.DataFrame(historical_data)
    dataframe.transpose()

    dataframe = pandas.DataFrame(historical_data)
    dataframe.transpose()
    dataframe.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    dataframe['datetime'] = dataframe.timestamp.apply(
        lambda x: pandas.to_datetime(datetime.fromtimestamp(x).strftime('%c'))
    )

    dataframe.set_index('datetime', inplace=True, drop=True)
    dataframe.drop('timestamp', axis=1, inplace=True)

    return dataframe


def analyze_macd(historial_data):
    """Performs a macd analysis on the historical data

    Args:
        historial_data (list): A matrix of historical OHCLV data.
    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    if type(historial_data) != pandas.core.frame.DataFrame:
        historial_data = convert_to_dataframe(historial_data)
    return abstract.MACD(historial_data).iloc[:, 0]


def analyze_rsi(historial_data, period_count=14):
    """Performs an RSI analysis on the historical data

    Args:
        historial_data (list): A matrix of historical OHCLV data.
        period_count (int, optional): Defaults to 14. The number of data points to consider for
            our simple moving average.
    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    indicator_name = 'rsi-{}'.format(period_count)

    if type(historial_data) != pandas.core.frame.DataFrame:
        historial_data = convert_to_dataframe(historial_data)

    rsi_values = abstract.RSI(historial_data, period_count)
    if indicator_name in historial_data:
        historial_data.drop(indicator_name, 1, inplace=True)

    combined_data = pandas.concat([historial_data, rsi_values], axis=1)
    combined_data.rename(columns={0: indicator_name}, inplace=True)
    return combined_data


def analyze_sma(historial_data, period_count=15):
    """Performs a SMA analysis on the historical data

    Args:
        historial_data (list): A matrix of historical OHCLV data.
        period_count (int, optional): Defaults to 15. The number of data points to consider for
            our simple moving average.
    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    indicator_name = 'sma-{}'.format(period_count)

    if type(historial_data) != pandas.core.frame.DataFrame:
        historial_data = convert_to_dataframe(historial_data)

    sma_values = abstract.SMA(historial_data, period_count)
    if indicator_name in historial_data:
        historial_data.drop(indicator_name, 1, inplace=True)

    combined_data = pandas.concat([historial_data, sma_values], axis=1)
    combined_data.rename(columns={0: indicator_name}, inplace=True)
    return combined_data


def analyze_ema(historial_data, period_count=15):
    """Performs an EMA analysis on the historical data

    Args:
        historial_data (list): A matrix of historical OHCLV data.
        period_count (int, optional): Defaults to 15. The number of data points to consider for
            our exponential moving average.
    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    indicator_name = 'ema-{}'.format(period_count)

    if type(historial_data) != pandas.core.frame.DataFrame:
        historial_data = convert_to_dataframe(historial_data)

    ema_values = abstract.EMA(historial_data, period_count)
    if indicator_name in historial_data:
        historial_data.drop(indicator_name, 1, inplace=True)

    combined_data = pandas.concat([historial_data, ema_values], axis=1)
    combined_data.rename(columns={0: indicator_name}, inplace=True)
    return combined_data


def analyze_bollinger_bands(historial_data, period_count=21):
    """Performs a bollinger band analysis on the historical data

    Args:
        historial_data (list): A matrix of historical OHCLV data.
        period_count (int, optional): Defaults to 21. The number of data points to consider for
            our bollinger bands
    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    if type(historial_data) != pandas.core.frame.DataFrame:
        historial_data = convert_to_dataframe(historial_data)

    return abstract.BBANDS(historial_data, period_count)
