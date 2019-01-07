from flask import Flask, request, jsonify, render_template
import traceback

from backtest import Backtester
from exchange import Exchange


"""
A server object wrapping our flask instance
"""
class Server(object):
    def __init__(self, exchange_interface):
        """Initialize our Server class.

        Args:
            exchange_interface (ExchangeInterface): Instance of the GDAX class for
                making exchange queries.
        """

        self.exchange_interface = exchange_interface

        self.app = Flask(__name__, static_folder='../www/static', template_folder='../www/static/templates')
        self.__add_backtesting_endpoints()

    def __add_backtesting_endpoints(self):

        def index_action():
            return render_template("index.html")

        def pairs_action():
            pairs = self.exchange_interface.get_available_keypairs()
            return jsonify(response=200, result=pairs)

        def backtesting_action():
            # Our Exchange client only accepts coin pairs separated by a '-', not '/'
            coin_pair = request.args.get('pair').replace('/', '-')
            period_length = request.args.get('period')
            capital = float(request.args.get('capital'))
            stop_loss = float(request.args.get('stopLoss'))
            start_time = int(request.args.get('startTime'))

            post_data = request.get_json()
            indicators = post_data['indicators']
            buy_strategy = post_data['buyStrategy']
            sell_strategy = post_data['sellStrategy']

            try:
                backtester = Backtester(coin_pair, period_length, self.exchange_interface, capital, stop_loss,
                                        buy_strategy, sell_strategy, start_time, indicators)
                backtester.run()
                result = backtester.get_results()

                return jsonify(response=200, result=result)

            except Exception as e:

                # Return the exception message if the selected exchange encounters an error while fetching historical data
                return jsonify(response=500, result={'message': str(e), 'stack_trace': traceback.format_exc()})

        self.add_endpoint(endpoint='/', endpoint_name='index', handler=index_action)
        self.add_endpoint(endpoint='/backtest', endpoint_name='backtest', methods=['POST'], handler=backtesting_action)
        self.add_endpoint(endpoint='/pairs', endpoint_name='pairs', handler=pairs_action)

    def run(self, debug=False):
        import os
        port = int(os.environ.get('PORT', 5000))
        self.app.run(debug=debug, host='0.0.0.0', port=port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, methods=['GET'], handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)


class EndpointAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        return self.action()

if __name__ == '__main__':
    exchange = Exchange()
    server = Server(exchange)
    server.run()
