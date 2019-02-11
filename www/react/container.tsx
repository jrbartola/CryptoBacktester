import * as React from 'react';

import { Navbar } from './navbar';
import { Dashboard } from './dashboard';

interface ContainerProps {}
interface ContainerState {}

export class Container extends React.Component<ContainerProps, ContainerState> {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div id="container">
			    <Navbar />
			    <Dashboard />
			</div>
		)
	}
}