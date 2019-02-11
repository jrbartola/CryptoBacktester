import * as React from "react";

interface IndicatorProps { shownIndicators: Set<string>, updateIndicators: (s: Set<string>) => void }
interface IndicatorState {}

/**
 * Defines the right indicator pane within the control panel on the dashboard
 */
export class IndicatorPane extends React.Component<IndicatorProps, IndicatorState> {
    constructor(props) {
        super(props);

        this.addRemoveCheck = this.addRemoveCheck.bind(this);
    }


    /**
     * Adds or removes a check for the given indicator specified.
     *
     * @param {string} value: The json string representation of the modified indicator
     * @param {boolean} checked: True if the indicator should be shown, false if it should be removed
     */
    private addRemoveCheck(value: string, checked: boolean): void {
        if (checked) {
            this.props.updateIndicators(this.props.shownIndicators.add(value));
        } else {
            const updated = [...this.props.shownIndicators.values()].filter(i => i !== value);
            this.props.updateIndicators(new Set<string>(updated));
        }
    }

    render() {
        return (
            <div className="card-body">
                <form action="#">
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" id="bbands-box"
                             checked={this.props.shownIndicators.has("bollinger-21-2")}
                             onChange={(e) => this.addRemoveCheck("bollinger-21-2", e.target.checked)}/>
                      <label className="form-check-label" htmlFor="bbands-box">Bollinger Bands</label>
                    </div>
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" id="ma-9-box"
                             checked={this.props.shownIndicators.has("sma-9")}
                             onChange={(e) => this.addRemoveCheck("sma-9", e.target.checked)} />
                      <label className="form-check-label" htmlFor="ma-9-box">Moving Average (9 Period)</label>
                    </div>
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" id="ma-15-box"
                             checked={this.props.shownIndicators.has("sma-15")}
                             onChange={(e) => this.addRemoveCheck("sma-15", e.target.checked)} />
                      <label className="form-check-label" htmlFor="ma-15-box">Moving Average (15 Period)</label>
                    </div>
                    {/*<p>*/}
                      {/*<input type="checkbox" id="macd" defaultChecked={showIndicators.macd} />*/}
                      {/*<label htmlFor="macd">MACD</label>*/}
                    {/*</p>*/}
                    {/*<p>*/}
                      {/*<input type="checkbox" id="rsi" defaultChecked={showIndicators.rsi} />*/}
                      {/*<label htmlFor="rsi">Relative Strength Index</label>*/}
                    {/*</p>*/}
                </form>
            </div>
        );
    }
}