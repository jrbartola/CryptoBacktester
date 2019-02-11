import * as React from "react";
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

interface CoinProps { coinPairs: string[], timeUnits: string[], selectedPair: string,
                      selectedTime: string, startTime: Date, stopLoss: string, capital: string,
                      updateCoinState: (newState) => void}
interface CoinState {  }

/**
 * Defines the left coin pane within the control panel on the dashboard
 */
export class CoinPane extends React.Component<CoinProps, CoinState> {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="card-body strategy-container">
                <div className="row">
                 <div className="input-field col-md-6">
                 <select value={this.props.selectedPair} id="coin-pair" className="form-control"
                         onChange={(e) => this.props.updateCoinState({selectedPair: e.target.value})}>
                     { this.props.coinPairs.map(pair =>
                         <option key={pair} value={pair}>{pair}</option>
                     )}
                 </select>
                 <label htmlFor="coin-pair">Coin Pair</label>
                 </div>
                 <div className="input-field col-md-6">
                   <input value={this.props.capital} placeholder="Eg: 0.01" id="amount-btc" type="text"
                          onChange={(e) => this.props.updateCoinState({capital: e.target.value})}
                          className="form-control" />
                   <label className="active" htmlFor="amount-btc">Capital</label>
                 </div>
                </div>
                <div className="row">
                 <div className="input-field col-4">
                   <select value={this.props.selectedTime} id="time-unit" className="form-control"
                           onChange={(e) => this.props.updateCoinState({selectedTime: e.target.value})}>
                     { this.props.timeUnits.map(unit =>
                         <option key={unit} value={unit}>{unit}</option>
                     )}
                   </select>
                   <label>Time Unit</label>
                 </div>
                 <div className="input-field col-8">
                     <DatePicker
                        selected={this.props.startTime}
                        onChange={(date) => this.props.updateCoinState({startTime: date})}
                        />
                   <label className="active" htmlFor="start-time">Start Time</label>
                 </div>
                </div>
                <div className="row">
                  <div className="input-field col s6">
                   <input value={this.props.stopLoss} id="stop-loss" type="text" className="form-control"
                          onChange={(e) => this.props.updateCoinState({stopLoss: e.target.value})}/>
                   <label className="active" htmlFor="stop-loss">Stop Loss (%)</label>
                  </div>
               </div>
            </div>
        );
    }
}