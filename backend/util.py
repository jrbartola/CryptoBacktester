"""
Contains utility functions to help with parsing OHLCV data
"""


def epoch_to_str(epoch_time):
    """
    Converts from epoch time (in seconds) to an ISO-1806 timestamp
    Args:
        epoch_time (int | float): A numerical value representing the seconds since epoch
    Returns:
        str: A string representation of the given time in ISO-1806 format
    """
    import time

    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))


def period_to_integer(period):
    """
    Converts a period string into a integer
    Args:
        period (str): A string denoting the period of time each candlestick represents (i.e., '15m')
    Returns:
        int: An integer denoting the period of time in seconds
    """

    import re

    try:
        num_units = re.findall(r'\d+', period)[0]
        unit_type = period[len(num_units):]
        if unit_type == 'm':
            return 60 * int(num_units)
        if unit_type == 'h':
            return 60 * 60 * int(num_units)
        if unit_type == 'd':
            return 24 * 60 * 60 * int(num_units)

    except IndexError:
        raise ValueError("`Period` string should contain a character prefixed with an integer")


def serialize_ohlcv(ohlcv_matrix):
    """
    Maps a OHLCV dataframe into a python dictionary

    Args:
        ohlcv_matrix (pandas.DataFrame): A pandas dataframe containing OHLCV + indicator data
    Returns:
        list[dict[str,-]]: A dictionary mapping ohlcv column strings to their values
    """

    # Map each row in the dataframe to a dictionary representation
    json_dataframe = []
    for index, row in ohlcv_matrix.iterrows():
        datum = {'time': index.value // 1e9, **{col: row[col] for col in row.index}}
        json_dataframe.append(datum)

    return json_dataframe
