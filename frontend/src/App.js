import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Leaderboard from './Leaderboard';
import Privacy from './Privacy';
import Terms from './Terms';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/leaderboard" element={<Leaderboard />}  />
        <Route path="/privacy" element={<Privacy />}  />
        <Route path="/terms" element={<Terms />}  />
      </Routes>
    </Router>
  );
}

export default App;
