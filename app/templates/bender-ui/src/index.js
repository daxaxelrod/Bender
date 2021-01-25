import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Welcome from './components/Welcome';
import Selection from './components/Selection';
import Enjoy from './components/Enjoy';
import 'bulma/css/bulma.css'

import {
  BrowserRouter as Router,
  Switch, Route } from "react-router-dom";


ReactDOM.render(
  <React.StrictMode>    
    <Router>
        <Switch>
          <Route path="/finished" exact>
            <Enjoy />
          </Route>
          <Route path="/drinks" exact>
            <Selection />
          </Route>
          <Route path="/" exact>
            <Welcome />
          </Route>
        </Switch>
    </Router>

  </React.StrictMode>,
  document.getElementById('root')
);