// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './HeaderBar';
import About from './About';
import Leaderboard from './Leaderboard';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route exact path="" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/leaderboard" component={Leaderboard} />
      </Switch>
    </Router>
  );
}

export default App;
