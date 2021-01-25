import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Welcome from './components/Welcome';
import Selection from './components/Selection';
import Enjoy from './components/Enjoy';
import 'bulma/css/bulma.css';
import 'react-activity/dist/react-activity.css';
import drink_1 from './stock_drink_1.jpeg'

import {
  BrowserRouter as Router,
  Switch, Route
} from "react-router-dom";


ReactDOM.render(
  <React.StrictMode>
    <div className="hero is-fullheight has-background-dark has-background">
      <img alt="Fill Murray" className="hero-background is-transparent" src={drink_1} />
      <div className="hero-body">

        <Router>
          <Switch>
            <Route path="/enjoy" exact>
              <Enjoy />
            </Route>
            <Route path="/drinks" exact>
              <Selection />
            </Route>
            <Route path="/">
              <Welcome />
            </Route>
          </Switch>
        </Router>

      </div>
    </div>


  </React.StrictMode>,
  document.getElementById('root')
);