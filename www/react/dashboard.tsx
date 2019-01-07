import * as React from "react";
import Swal from "sweetalert2";
import {GETRequest} from "./util/http";

// import ControlPanel from './ControlPanel.jsx';
// import Plot from './Plot.jsx';

interface DashboardProps { }
interface DashboardState { coinPairs: string[], timeUnits: string[], showIndicators: Map<string, boolean>,
                           indicators: Map<string, number[]>, closingPrices: number[], buys: number[], sells: number[],
                           profit: number }

/**
 * The Dashboard component contains the entire home page of the crypto backtester/bot
 */
export class Dashboard extends React.Component<DashboardProps, DashboardState> {
	constructor(props) {
		super(props);

		this.state = {
		    coinPairs: ["ETH/BTC", "LTC/BTC", "XRP/BTC"],
            timeUnits: ["1m", "5m", "15m", "1h", "6h", "1d"],
            showIndicators: new Map<string, boolean>([["bollinger", false],
                                                     ["sma9", true],
                                                     ["sma15", false],
                                                     ["macd", false],
                                                     ["rsi", false]]),
		    indicators: new Map<string, number[]>([["bollinger_upper", []],
                                                  ["bollinger_lower", []],
                                                  ["macd", []],
                                                  ["rsi", []],
                                                  ["sma9", []],
                                                  ["sma15", []]]),
            closingPrices: [],
            buys: [],
            sells: [],
            profit: 0
        };

        this.getBacktestingData = this.getBacktestingData.bind(this);
        this.getMarketPairs = this.getMarketPairs.bind(this);

        setTimeout(this.getMarketPairs(), 1000);


	}


    /** Retrieves coin pair data for the GDAX exchange
     *
     */
    getMarketPairs() {
        GETRequest(`${window.location.origin}/pairs`).then(resp => {
            const pairs: string[] = resp["data"];
            this.setState({coinPairs: pairs});
        }).catch(errResp => {
            console.error(`Something went wrong while fetching coin pairs. (${errResp}`);
            Swal("Uh oh", `Something went wrong while fetching coin pairs. (${errResp})`, "error");
        });
    }

    /** Retrieves backtesting results from the server
     *
     * @param coinPair: A trading pair whose historical data is to be retrieved
     * @param timeUnit: The time unit to extract from historical data (minute, hour, day, etc.)
     * @param capital: The amount of Bitcoin to start out with
     * @param startTime: The starting time in epoch seconds
     * @param stopLoss: The amount of BTC below the initial buy position to set a stop loss at
     * @param buyStrategy: An object containing the buy strategy for this set of backtesting data
     * @param sellStrategy: An object containing the sell strategy for this set of backtesting data
     * @param indicators: An object containig key-value pairs of indicators and their parameters.
     */
	getBacktestingData(coinPair, timeUnit, capital, startTime, stopLoss, buyStrategy, sellStrategy, indicators) {

	    const url = `${window.location.origin}/backtest?pair=${coinPair}&period=${timeUnit}$
                    &capital=${capital}&stopLoss=${stopLoss}&startTime=${startTime}`;

	    const target = document.getElementById("d3plot");
        // const spinner = new Spinner(this.spinnerOpts).spin(target);

	    $.ajax({
            type: "POST",
            contentType: "application/json",
            url: url,
            dataType: "json",
            data: JSON.stringify({indicators: indicators, buyStrategy: buyStrategy, sellStrategy: sellStrategy}),
            success: data => {

                const responseCode = data["response"];

                if (responseCode === 200) {
                    console.log("Got backtesting data:", data);

                    const result = data["result"];

                    this.setState({
                        coinPairs: this.state.coinPairs,
                        closingPrices: result["closingPrices"],
                        buys: result["buys"],
                        sells: result["sells"],
                        indicators: result["indicators"],
                        profit: result["profit"]
                    });

                } else {
                    const errMsg = data["result"]["message"];

                    document.getElementById("d3plot").innerHTML = "";
                    swal("Uh oh!", "Something went wrong. Response code: " + responseCode + "<br/> . <strong>Error Message:</strong> \"" + errMsg + "\"", "error");
                }

            },
            error: res => {

                console.error(res);

                document.getElementById("d3plot").innerHTML = "";
                swal("Uh oh!", "Something went wrong: Response code " + res.status + ". Please try again.", "error");
            }
        });
    }

	render() {
		return (
			<div id="dashboard">
			  <div className="row">
			    <ControlPanel getBacktestingData={this.getBacktestingData} getMarketPairs={this.getMarketPairs}
                              coinPairs={this.state.coinPairs} profit={this.state.profit} timeUnits={this.state.timeUnits} showIndicators={this.state.showIndicators} />
			  </div>
			  <Plot closingPrices={this.state.closingPrices} buys={this.state.buys} sells={this.state.sells}
                  indicators={this.state.indicators} showIndicators={this.state.showIndicators} />
			</div>
		)
	}
}

export default Dashboard;