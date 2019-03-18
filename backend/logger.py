import datetime


def log(message, type="info"):
    """
    Logs the given message with a specified message typ
    Args:
        message (str): A message to be logged to the console
        type (str): One of ['success', 'info', 'warning', or 'error']. Will color the text appropriately
    """

    timestamp = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    message = "[ {} ]  ".format(timestamp) + message

    if type == 'success':
        message = "\033[1;33;92m" + message + "\033[0m"
    elif type == 'warning':
        message = "\033[1;33;93m" + message + "\033[0m"
    elif type == 'error':
        message = "\033[1;33;91m" + message + "\033[0m"

    print(message)
