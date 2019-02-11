import * as React from 'react';
import * as moment from 'moment';

import { ResponsiveContainer, ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Scatter } from 'recharts';
import { BacktestData } from "./types/conditions";

interface PlotProps { backtestData: BacktestData[], shownIndicators: Set<string> }
interface PlotState {}


export class Plot extends React.Component<PlotProps, PlotState> {
    constructor(props) {
        super(props);

    }

    static formatXAxis(tick): string {
        return moment(tick).format('MM/D/YY');
    }

    static makeLine(indicator): JSX.Element {
        const alphabet = "0123456789ABCDEF";
        const randomColor = [...Array(6).keys()]
            .map(_ => alphabet[Math.floor(Math.random() * 16)]).join('');

        return <Line key={indicator} type="linear" label={indicator} dataKey={"indicators." + indicator}
                     stroke={'#' + randomColor} strokeWidth={2} dot={false} />
    }

    render() {
        return (
            <div className="row">
                <div id="plot">
                    <ResponsiveContainer height={300} width="100%">
                           <ComposedChart data={this.props.backtestData} margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                           <XAxis dataKey="time" type="number" tickFormatter={Plot.formatXAxis} scale="time" domain={['dataMin', 'dataMax']} />
                           <YAxis dataKey="close" domain={['dataMin', 'dataMax']} />
                           <CartesianGrid strokeDasharray="3 3"/>
                           <Tooltip/>
                           <Legend />
                           <Line type="monotone" dataKey="close" stroke="#8884d8" strokeWidth={2} dot={false} />

                               { [...this.props.shownIndicators.values()].map(Plot.makeLine) }

                           <Line type="linear" dataKey="buy" stroke="green" legendType="circle" dot={{ stroke: 'green', strokeWidth: 3 }} />
                           <Line type="linear" dataKey="sell" stroke="red" legendType="circle" dot={{ stroke: 'red', strokeWidth: 3 }} />

                           {/*<Scatter data={this.props.backtestData} dataKey="buy" fill="green" activeDot={{r: 6}} />*/}
                           {/*<Scatter data={this.props.backtestData} dataKey="sell" fill="red" activeDot={{r: 6}} />*/}
                          </ComposedChart>
                      </ResponsiveContainer>
                </div>
            </div>

        )
    }

}