import * as React from 'react';

interface NavProps {}
interface NavState {}

export class Navbar extends React.Component<NavProps, NavState> {
	constructor(props) {
		super(props);

	}

	render() {
		return (
			<nav>
              <div className="nav-wrapper">
              <a href="#" className="brand-logo">CryptoBot</a>
              </div>
            </nav>
		)
	}
}