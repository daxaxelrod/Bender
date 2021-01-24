import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Welcome from './components/Welcome';
import Selection from './components/Selection';
import Enjoy from './components/Enjoy';
import {
  BrowserRouter as Router,
  Switch, Route } from "react-router-dom";


ReactDOM.render(
  <React.StrictMode>    
    <Router>
        <Switch>
          <Route path="/finished">
            <Enjoy />
          </Route>
          <Route path="/drinks">
            <Selection />
          </Route>
          <Route path="/">
            <Welcome />
          </Route>
        </Switch>
    </Router>

  </React.StrictMode>,
  document.getElementById('root')
);