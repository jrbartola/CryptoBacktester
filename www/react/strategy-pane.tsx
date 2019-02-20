import * as React from "react";

import {ConditionType} from "./types/conditions";
import {parse} from "./util/parser/parser";


interface StrategyProps { buyQuery: string, sellQuery: string, addCondition: (kind: ConditionType) => void,
                          removeCondition: (kind: ConditionType) => void, updateConditions: (kind: ConditionType, newQuery: string) => void }
interface StrategyState { buyParsed: boolean, sellParsed: boolean }


/**
 * Defines the middle strategy pane within the control panel on the dashboard
 */
export class StrategyPane extends React.Component<StrategyProps, StrategyState> {
    constructor(props) {
        super(props);

        // Assume the programmer will always set a valid condition query as the initial state ;)
        this.state = {buyParsed: true, sellParsed: true};

        this.onConditionChanged = this.onConditionChanged.bind(this);
    }

    /**
     * Executes when an input condition field is changed
     *
     * @param {string} newValue: The new value of the field
     * @param {ConditionType} kind: The condition kind (either buy or sell)
     */
    onConditionChanged(newValue: string, kind: ConditionType): void {
        this.props.updateConditions(kind, newValue);

        // Don't show a success or failure icon if there is no text in the condition box
        if (!newValue) {
            const newState = kind === ConditionType.BUY ? {buyParsed: null} : {sellParsed: null};
            this.setState({...newState});
            return;
        }

        const queryExp = parse(newValue);
        console.log(JSON.stringify(queryExp));
        switch (kind) {
            case ConditionType.BUY:
                this.setState({buyParsed: queryExp !== undefined});
                break;
            case ConditionType.SELL:
                this.setState({sellParsed: queryExp !== undefined});
                break;
            default:
                throw new Error("Argument `kind` must either be of type ConditionType.BUY or ConditionType.SELL");
        }
    }

    render() {
        // Setup the icons next to our condition input boxes so the user knows whether the condition queries parsed
        let buyClass = "fa fa-ban fa-1p5x";
        let buyTooltip = "Buy condition input required";
        let sellClass = "fa fa-ban fa-1p5x";
        let sellTooltip = "Sell condition input required";

        if (this.state.buyParsed !== null) {
            buyClass = this.state.buyParsed ? "fa fa-check-circle fa-1p5x" : "fa fa-exclamation-triangle fa-1p5x";
            buyTooltip = this.state.buyParsed ? "Condition parsed successfully" : "Malformed condition. See documentation";
        }
        if (this.state.sellParsed !== null) {
            sellClass = this.state.sellParsed ? "fa fa-check-circle fa-1p5x" : "fa fa-exclamation-triangle fa-1p5x";
            sellTooltip = this.state.buyParsed ? "Condition parsed successfully" : "Malformed condition. See documentation";
        }

        return (
            <div className="input-field col-md-12 card-body strategy-container">
                <div className="input-field form-group col s6">
                    <label className="control-label" htmlFor="buy-when">Buy When</label>
                    <div className="input-group-append">
                        <input type="text" className="form-control" id="buy-when" value={this.props.buyQuery}
                              onChange={(e) => this.onConditionChanged(e.target.value, ConditionType.BUY)}/>
                        <span className="input-group-text" title={buyTooltip}>
                            <i className={buyClass}></i>
                        </span>
                    </div>
                </div>


                <div className="input-field form-group col s6">
                   <label className="active" htmlFor="sell-when">Sell When</label>
                    <div className="input-group-append">
                        <input type="text" className="form-control" id="sell-when" value={this.props.sellQuery}
                              onChange={(e) => this.onConditionChanged(e.target.value, ConditionType.SELL)}/>
                        <span className="input-group-text" title={sellTooltip}>
                            <i className={sellClass}></i>
                        </span>
                    </div>

                </div>
            </div>
        );
    }
}