import * as React from 'react';
import * as moment from 'moment';

import { ResponsiveContainer, ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Scatter } from 'recharts';
import { BacktestData } from "./types/conditions";

interface PlotProps { backtestData: BacktestData[], shownIndicators: Set<string> }
interface PlotState {}

/**
 * Defines the cartesian plot under the control panel, displaying closing prices and indicators
 */
export class Plot extends React.Component<PlotProps, PlotState> {
    constructor(props) {
        super(props);

    }

    static formatDateLabel(datestr): (string) => string {
        return (tick) => moment(tick).format(datestr);
    }

    static makeLine(indicator): JSX.Element {
        const alphabet = "0123456789ABCDEF";
        const randomColor = [...Array(6).keys()]
            .map(_ => alphabet[Math.floor(Math.random() * 16)]).join('');

        return <Line key={indicator} type="linear" name={indicator} dataKey={"indicators." + indicator}
                     stroke={'#' + randomColor} strokeWidth={2} dot={false} />
    }

    render() {
        return (
            <div className="row">
                <div id="plot">
                    <ResponsiveContainer height={300} width="100%">
                           <ComposedChart data={this.props.backtestData} margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                           <XAxis dataKey="time" type="number" tickFormatter={Plot.formatDateLabel('MM/D/YY')} scale="time" domain={['dataMin', 'dataMax']} />
                           <YAxis dataKey="close" domain={['dataMin', 'dataMax']} />
                           <CartesianGrid strokeDasharray="3 3"/>
                           <Tooltip formatter={(value, name) => Math.round(value * 1e6) / 1e6} labelFormatter={Plot.formatDateLabel('MM/D/YY LT')}/>
                           <Legend />
                           <Line type="monotone" dataKey="close" stroke="#8884d8" strokeWidth={2} dot={false} />

                               { [...this.props.shownIndicators.values()].map(Plot.makeLine) }

                           <Line type="linear" dataKey="buy" stroke="green" legendType="circle" dot={{ stroke: 'green', strokeWidth: 3 }} />
                           <Line type="linear" dataKey="sell" stroke="red" legendType="circle" dot={{ stroke: 'red', strokeWidth: 3 }} />

                          </ComposedChart>
                      </ResponsiveContainer>
                </div>
            </div>

        )
    }

}