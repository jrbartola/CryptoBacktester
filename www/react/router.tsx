import * as React from "react";
import { Switch, Route } from "react-router-dom";

import { Container } from "./container";

/** App will be the main container for the entire front end **/
export const App = () => (
    <Switch>
        <Route exact path='/' component={Container} />
    </Switch>
);