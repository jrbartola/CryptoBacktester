import * as React from "react";
import Swal from "sweetalert2";
import { GETRequest, POSTRequest } from "./util/http";

import { ControlPanel } from './control-panel';
import { Plot } from './plot';
import {BacktestData, BacktestPayload} from "./types/conditions";

interface DashboardProps { }
interface DashboardState { coinPairs: string[], timeUnits: string[], shownIndicators: Set<string>,
                           backtestData: BacktestData[], profit: number }

/**
 * The Dashboard component contains the entire home page of the crypto backtester
 */
export class Dashboard extends React.Component<DashboardProps, DashboardState> {
	constructor(props) {
		super(props);

		this.state = {
		    coinPairs: ["ETH/BTC", "LTC/BTC", "XRP/BTC"],
            timeUnits: ["1m", "5m", "15m", "1h", "6h", "1d"],
            shownIndicators: new Set<string>(["sma-9"]),
            backtestData: [],
            profit: 0
        };

        this.getBacktestingData = this.getBacktestingData.bind(this);
        this.mapBacktestResponse = this.mapBacktestResponse.bind(this);
        this.updateIndicators = this.updateIndicators.bind(this);

        this.getMarketPairs();
	}

	/**
     * Updates the set of shown indicator strings with a new set
     *
     * @param {Set<string>} newIndicators: A set denoting the list of visible indicators
     */
    updateIndicators(newIndicators: Set<string>): void {
        this.setState({shownIndicators: newIndicators});
    }

    /**
     * Retrieves coin pair data from the GDAX exchange
     */
    getMarketPairs() {
        GETRequest(`${window.location.origin}/pairs`).then(resp => {
            const pairs: string[] = resp['result'];
            this.setState({coinPairs: pairs});
        }).catch(errResp => {
            console.error(`Something went wrong while fetching coin pairs. (${errResp}`);
            Swal("Uh oh", `Something went wrong while fetching coin pairs. (${errResp})`, "error");
        });
    }

    /**
     * Retrieves backtesting data from the server
     *
     * @param {BacktestPayload} payload: The backtest payload object containing coin, strategy, and indicator information
     */
	getBacktestingData(payload: BacktestPayload) {
	    const URL = `${window.location.origin}/backtest?pair=${payload.coinPair}&period=${payload.timeUnit}` +
            `&capital=${payload.capital}&stopLoss=${payload.stopLoss}&startTime=${payload.startTime}`;
	    const jsonBody = {indicators: payload.indicators, buyStrategy: payload.buyStrategy, sellStrategy: payload.sellStrategy};

        POSTRequest(URL, jsonBody).then(resp => {
            console.log("Got backtesting data: ", resp);

            if (resp["response"] !== 200) {
                throw new Error(`Error occurred while fetching backtest results: ${resp["result"]["message"]}`);
            }

            const result = resp["result"];
            const backtestData = this.mapBacktestResponse(result);

            this.setState({
                backtestData: backtestData,
                profit: result["profit"]
            });
        }).catch(errResp => {
            Swal("Uh oh!", "Something went wrong: " + "<br/><strong>Error Message:</strong> \"" + errResp + "\"", "error");
            console.error(`An error occurred while submitting the search query (${errResp})`);
        });
    }

    /**
     * Maps the backtesting JSON response into an array of BacktestData
     *
     * @param {object} result: The response obtained from the backtesting API
     */
    private mapBacktestResponse(result: object): BacktestData[] {
        // Create a mapping from timestamp to closing price, indicators, buys, and sells
	    let timeMap = new Map<number, object>();
	    result["closingPrices"].forEach(([time, price]) => {
	        timeMap.set(time, {close: price});
        });

	    result["buys"].forEach(([time, price]) => {
	        timeMap.set(time, {...timeMap.get(time), buy: price})
        });

        result["sells"].forEach(([time, price]) => {
	        timeMap.set(time, {...timeMap.get(time), sell: price})
        });

        Object.keys(result["indicators"]).forEach(indicator => {
            result["indicators"][indicator].forEach(([time, value]) => {
                // Make sure we only include indicators for which we have corresponding closing times
                if (timeMap.has(time)) {
                    const indicators = timeMap.get(time)["indicators"] || {};
                    timeMap.set(time, {...timeMap.get(time), indicators: {...indicators, [indicator]: value}});
                }
            });
        });

        return [...timeMap.entries()].map(([time, data]) =>  {
            return {close: 0, ...data, time: time*1000} as BacktestData;
        }).sort((a, b) => a.time < b.time ? -1 : 1);
    }

	render() {
		return (
			<div id="dashboard" className="container-fluid">
			  <div className="row">
			    <ControlPanel coinPairs={this.state.coinPairs} timeUnits={this.state.timeUnits} profit={this.state.profit}
                              shownIndicators={this.state.shownIndicators} getBacktestingData={this.getBacktestingData}
                              updateIndicators={this.updateIndicators} />
			  </div>
                  <Plot backtestData={this.state.backtestData} shownIndicators={this.state.shownIndicators} />
			</div>
		)
	}
}