import * as React from "react";
import update from 'immutability-helper';

import {Comparator, Condition, ConditionType} from "./types/conditions";
import {DEFAULT_INDICATORS, Indicator, INDICATOR_MAP} from "./types/indicators";


interface StrategyProps { buyConditions: Condition[], sellConditions: Condition[], addCondition: (kind: ConditionType) => void,
                          removeCondition: (kind: ConditionType) => void, updateConditions: (kind: ConditionType, newConditions: Condition[]) => void }
interface StrategyState {}


/**
 * Defines the middle strategy pane within the control panel on the dashboard
 */
export class StrategyPane extends React.Component<StrategyProps, StrategyState> {
    constructor(props) {
        super(props);

        this.onDropdownChanged = this.onDropdownChanged.bind(this);
        this.onComparatorChanged = this.onComparatorChanged.bind(this);
        this.onValueChanged = this.onValueChanged.bind(this);
    }

    componentDidUpdate(prevProps: StrategyProps) {
        // console.log("PROPPPPS", prevProps, this.props);
    }

    /**
     * Executes when the state of the left-side indicator dropdown field is changed
     *
     * @param {string} newValue: The new value of the field
     * @param {ConditionType} kind
     * @param {number} idx
     */
    onDropdownChanged(newValue: string, kind: ConditionType, idx: number): void {
        let updatedConditions = kind === ConditionType.BUY ? [...this.props.buyConditions] : [...this.props.sellConditions];
        updatedConditions[idx] = update(updatedConditions[idx], {leftSide: {$set: INDICATOR_MAP.get(newValue) as Indicator }});
        this.props.updateConditions(kind, updatedConditions);
    }

    /**
     * Executes when the state of a buy/sell comparator is changed
     *
     * @param {string} newValue: The new value of the field
     * @param {ConditionType} kind
     * @param {number} idx
     */
    onComparatorChanged(newValue: string, kind: ConditionType, idx: number): void {
        let updatedConditions = kind === ConditionType.BUY ? [...this.props.buyConditions] : [...this.props.sellConditions];
        updatedConditions[idx] = update(updatedConditions[idx], {comparator: {$set: newValue as Comparator}});
        this.props.updateConditions(kind, updatedConditions);
    }

    /**
     * Executes when the state of a Value field (right-side) for a buy/sell condition is changed
     *
     * @param {string} newValue: The new value of the field
     * @param {ConditionType} kind
     * @param {number} idx
     */
    onValueChanged(newValue: string, kind: ConditionType, idx: number): void {
        let updatedConditions = kind === ConditionType.BUY ? [...this.props.buyConditions] : [...this.props.sellConditions];
        updatedConditions[idx] = update(updatedConditions[idx], {rightSide: {$set: INDICATOR_MAP.get(newValue) as Indicator}});
        this.props.updateConditions(kind, updatedConditions);
    }

    /**
     * Creates a condition row (indicator, comparator, indicator) with the given
     * condition type (buy or sell) and the index of that condition
     *
     * @param {ConditionType} kind
     * @param {number} idx
     */
    private makeConditionRow(kind: ConditionType, idx: number): JSX.Element {
        const currCondition = kind === ConditionType.BUY ? this.props.buyConditions[idx] :
                                                       this.props.sellConditions[idx];

        const leftSide = currCondition.leftSide ? currCondition.leftSide.jsonRepr() : "";
        const rightSide = currCondition.rightSide ? currCondition.rightSide.jsonRepr() : "";

        return (
            <div className="row">
                <div className="input-field col-sm-5">
                    <select className="form-control form-control-sm indicator-dropdown" value={leftSide}
                            onChange={(e) => this.onDropdownChanged(e.target.value, kind, idx)}>
                        { DEFAULT_INDICATORS.map((indicator, i) =>
                            <option key={`${indicator}-${i}`} value={indicator.jsonRepr()}>
                                { indicator.toString() }
                            </option>
                        )}
                    </select>
                    <label>{kind === ConditionType.BUY ? "Buy" : "Sell"} When</label>
                </div>
                <div className="input-field col-sm-2">
                    <select className="form-control form-control-sm comparator" value={currCondition.comparator.toString()}
                            onChange={(e) => this.onComparatorChanged(e.target.value, kind, idx)} >
                        <option value="<">&lt;</option>
                        <option value="=">=</option>
                        <option value=">">&gt;</option>
                    </select>
                </div>
                <div className="input-field col-sm-5">
                    <select className="form-control form-control-sm indicator-dropdown" value={rightSide}
                            onChange={(e) => this.onValueChanged(e.target.value, kind, idx)}>
                        { DEFAULT_INDICATORS.map((indicator, i) =>
                            <option key={`${indicator}-${i}`} value={indicator.jsonRepr()}>
                                { indicator.toString() }
                            </option>
                        )}
                    </select>
                  <label htmlFor={idx.toString()}>Value</label>
                </div>
            </div>
        );
    }

    /**
     * Creates the add/remove condition buttons
     *
     * @param {ConditionType} kind
     */
    private makeAddRemoveRow(kind: ConditionType): JSX.Element {
        const conditionLength = kind === ConditionType.BUY ? this.props.buyConditions.length :
                                                             this.props.sellConditions.length;

        return (
            <div className="row add-remove-container">
                 <a onClick={() => this.props.addCondition(kind)} className="btn btn-primary btn-sm add-remove-btn">
                     <i className="fa fa-plus"></i>
                 </a>

                {conditionLength > 1 &&
                    <a onClick={() => this.props.removeCondition(kind)} className="btn btn-primary btn-sm add-remove-btn">
                        <i className="fa fa-minus"></i>
                    </a>
                }
             </div>
        )
    }

    render() {
        return (
            <div className="input-field col-md-12 card-body strategy-container">
                 { this.props.buyConditions.map((_, i) =>
                     <div key={i}>
                         { this.makeConditionRow(ConditionType.BUY, i) }
                     </div>
                 )}

                 { this.makeAddRemoveRow(ConditionType.BUY) }

                 { this.props.sellConditions.map((_, i) =>
                     <div key={i}>
                         { this.makeConditionRow(ConditionType.SELL, i) }
                     </div>
                 )}

                 { this.makeAddRemoveRow(ConditionType.SELL) }

            </div>
        );
    }
}