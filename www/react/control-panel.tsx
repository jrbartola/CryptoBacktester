import * as React from 'react';
import Swal from 'sweetalert2'

import {BacktestPayload, Comparator, Condition, ConditionType} from "./types/conditions";
import {StrategyPane} from "./strategy-pane";
import {IndicatorPane} from "./indicator-pane";
import {CoinPane} from "./coin-pane";
import {evaluateIndicators, parse} from "./util/parser/parser";


interface ControlProps { coinPairs: string[], timeUnits: string[], profit: number, shownIndicators: Set<string>,
                         getBacktestingData: (...params: Object[]) => void, updateIndicators: (s: Set<string>) => void }
interface ControlState { buyQuery: string, sellQuery: string, selectedPair: string,
                         selectedTime: string, startTime: Date, stopLoss: string, capital: string }

/**
 * Defines the control panel on the upper dashboard, allowing user to adjust backtesting parameters
 */
export class ControlPanel extends React.Component<ControlProps, ControlState> {

    constructor(props) {
       super(props);

       const firstPair = this.props.coinPairs.length > 0 ? this.props.coinPairs[0] : "No pairs";
       const firstTime = this.props.timeUnits.length > 0 ? this.props.timeUnits[0] : "No times";

       this.state = {
                     buyQuery: "current-price > sma(9)",
                     sellQuery: "current-price < sma(9)",
                     selectedPair: firstPair,
                     selectedTime: firstTime,
                     startTime: new Date(),
                     stopLoss: "",
                     capital: ""
                    };


       this.updateConditions = this.updateConditions.bind(this);
       this.updateCoinState = this.updateCoinState.bind(this);
       this.parseStrategies = this.parseStrategies.bind(this);
       this.requestBacktest = this.requestBacktest.bind(this);

   }

   /**
     * Updates the coin information state
    *
     * @param {CoinState} newState: A state object containing one or more of the following fields containing coin data:
     *   `selectedPair`, `selectedTime`, `startTime`, `stopLoss`, and `capital`
     */
   updateCoinState(newState: object): void {
       this.setState(newState);
   }

   /**
    * Updates the buy/sell condition state
    *
    * @param {ConditionType} kind: An enum value describing whether to update a Buy or Sell condition
    * @param {Condition[]} newQuery: The updated condition query
    */
   updateConditions(kind: ConditionType, newQuery: string): void {
       switch (kind) {
           case ConditionType.BUY:
               this.setState({buyQuery: newQuery});
               break;
           case ConditionType.SELL:
               this.setState({sellQuery: newQuery});
               break;
           default:
               throw new Error("Argument `kind` must either be of type ConditionType.BUY or ConditionType.SELL");
       }
   }

    /**
     * Parses the 'capital' and 'stop loss' coin fields. Shows a modal if we are given improper input, otherwise
     * return the capital and stop loss as numbers
     *
     * @returns {[number, number]}: The capital and stop loss, respectively
     */
   private parseCoinInfo(): [number, number] {
       const capital = this.state.capital;
       const stopLoss = this.state.stopLoss;

       // Make sure the user has entered valid numbers for the capital and stop loss fields
       const capitalReg = /(^[1-9][0-9]*$)|(^[0-9]*\.[0-9]*$)/;
       const stopLossReg = /(^(100)$|(^[0-9]?[0-9](\.[0-9]+)?$))/;

       if (!capitalReg.exec(capital)) {
           Swal("Uh Oh!", "You need to enter a valid number for your starting capital.", "error");
           throw new Error("Invalid Capital");
       }

       if (stopLoss !== "" && !stopLossReg.exec(stopLoss)) {
           Swal("Uh Oh!", "You need to enter a valid percentage (0 - 100) for your stop loss.", "error");
           throw new Error("Invalid Stop Loss");
       }

       return [Number(capital), Number(stopLoss)];
   }

    /**
     * Serializes the list of buy and sell conditions into a stringified JSON payload object.
     *
     * @returns {[string, string, string[]]}: A serialized buy and serialized sell object, and set of indicators respectively.
     */
   private parseStrategies(): [string, string, Set<string>] {
       const parsedBuy = parse(this.state.buyQuery);

       if (!parsedBuy) {
           Swal("Uh Oh!", "You have not entered a valid buy condition. See documentation for help", "error");
           throw new Error("Invalid Buy Condition");
       }

       const parsedSell = parse(this.state.sellQuery);

       if (!parsedSell) {
           Swal("Uh Oh!", "You have not entered a valid sell condition. See documentation for help", "error");
           throw new Error("Invalid Sell Condition");
       }

       // Cast indicator array to set to remove duplicates
       const indicators = new Set(evaluateIndicators(parsedBuy).concat(evaluateIndicators(parsedSell));

       return [JSON.stringify(parsedBuy), JSON.stringify(parsedSell), indicators];
   }

    /**
     *  Requests a backtest by parsing state variables from the control panel and turning them into a backtest payload
     */
   private requestBacktest(): void {
       const [capital, stopLoss] = this.parseCoinInfo();
       const [buyStrategy, sellStrategy, indicators] = this.parseStrategies();

       const backtestData: BacktestPayload = {coinPair: this.state.selectedPair,
                                              timeUnit: this.state.selectedTime,
                                              capital: capital,
                                              stopLoss: stopLoss,
                                              startTime: Math.round(this.state.startTime.getTime() / 1000),
                                              buyStrategy: buyStrategy,
                                              sellStrategy: sellStrategy,
                                              indicators: [...indicators.values()]};

       this.props.getBacktestingData(backtestData);
   }

   render() {

       return (
                <div className="col-md-12 col-sm-12">
                  <div className="card">
                    <div className="card-body">
                        <div className="row">
                          <div className="card col-md-3 card-pane">
                            <h5 className="card-header">Coin Info</h5>
                            <CoinPane coinPairs={this.props.coinPairs} timeUnits={this.props.timeUnits}
                                      updateCoinState={this.updateCoinState} selectedPair={this.state.selectedPair}
                                      selectedTime={this.state.selectedTime} stopLoss={this.state.stopLoss}
                                      capital={this.state.capital} startTime={this.state.startTime}/>
                          </div>
                          <div className="card col-md-5 card-pane">
                            <h5 className="card-header">Strategy</h5>
                            <StrategyPane buyQuery={this.state.buyQuery}
                                          sellQuery={this.state.sellQuery}
                                          updateConditions={this.updateConditions} />
                          </div>
                          <div className="card col-md-3 card-pane">
                            <h5 className="card-header">Plot</h5>
                              <IndicatorPane shownIndicators={this.props.shownIndicators} updateIndicators={this.props.updateIndicators} />
                          </div>
                        </div>
                    </div>
                    <div className="card-footer">
                        <a className="btn btn-primary" id="start-btn" role="button" onClick={this.requestBacktest}>Start</a>
                      <h5 className="right">Profit: {this.props.profit} BTC</h5>
                    </div>
                  </div>
                </div>
       )
   }



}