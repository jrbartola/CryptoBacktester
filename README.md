# CryptoBacktester
A backtesting engine for testing trading strategies over GDAX (Coinbase Pro) marketplace data

![Alt text](/backtester.png "The dashboard")

This tool allows you to try different strategies over sets of historical trading data from Coinbase.

## Installation

First, clone or download the repository to your computer.

**Front End**- Navigate to the *www* directory and run `npm install`. Make sure you have the latest version of node.js installed on your computer.

**Back End**- The server should run with python 3.x. The dependencies are listed in the requirements.txt file, so just do a quick `pip install -r requirements.txt`.

## Running the Application

First, you'll need to use webpack to bundle all of the React .tsx files on the front end. Within the *www* directory run `npm run build`.

Next, navigate to the *backend* directory and run `python server.py`. Now you're all set! Open up your favorite browser and navigate to http://localhost:5000/ and try it out.

## How does it work?

Begin by selecting the coin pair you want to trade with. The first coin (the one before the "/") is the base currency-- the one you will be purchsing. The second coin is the quote currency, which is what you will use to buy the base currency. For example, if the coin pair is "ETH/BTC", you will be purchasing ETH using BTC.

"Capital" is the amount of quote currency you want to start out with trading.

"Time Unit" is the duration between each point on the time series of historical data.

"Stop Loss" (optional) is the percentage of base currency below each buy price that you will sell your position at. The smaller the stop loss, the less your risk.

"Start Time" is the starting date that the backtesting engine will run a strategy over.

Once you've filled out all of the fields, click "Start" to begin the backtesting. Your profit is shown in the bottom-right corner of the upper panel.

## What's on the Graph?

Green dots represent buy points. Red dots represent sell points. The purple line is the plot of historical closing prices, and any other indicators will appear as random colors designated by the legend on the plot.

## Coming Soon

RSI & MACD indicators, live trading strategies over Coinbase Pro, position report of buys/sells after backtesting
