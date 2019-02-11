import * as React from 'react';

interface NavProps {}
interface NavState {}

export class Navbar extends React.Component<NavProps, NavState> {
	constructor(props) {
		super(props);

	}

	render() {
		return (
			<nav className="navbar navbar-light bg-primary">
				<a className="navbar-brand">Crypto Backtester</a>
            </nav>
		)
	}
}