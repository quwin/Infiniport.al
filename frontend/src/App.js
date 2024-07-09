import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tableName, setTableName] = useState('total');
  const [order, setOrder] = useState('level');
  const [serverId, setServerId] = useState('');
  const [leaderboard, setLeaderboard] = useState([]);
  const SKILLS = [
      'forestry',
      'woodwork',
      'cooking',
      'mining',
      'exploration',
      'farming',
      'stoneshaping',
      'petcare',
      'business',
      'metalworking',
  ];

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    let url = `/leaderboard/${tableName}/${order}/1`;
    if (serverId) {
      url += `/${serverId}`;
    }

    try {
      console.log(url)
      const response = await axios.get(url);
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  return (
    <div className="App">
      <h1>Leaderboard</h1>
      <select value={tableName} onChange={(e) => setTableName(e.target.value)}>
        <option value="total">Overall</option>
        {SKILLS.map((skill) => (
          <option key={skill} value={skill}>
            {skill.charAt(0).toUpperCase() + skill.slice(1)}
          </option>
        ))}

      </select>
      <select value={order} onChange={(e) => setOrder(e.target.value)}>
        <option value="level">Level</option>
        <option value="exp">Experience</option>
      </select>
      <input
        type="text"
        value={serverId}
        onChange={(e) => setServerId(e.target.value)}
        placeholder="Server ID (optional)"
      />
      <button onClick={fetchLeaderboard}>Get Leaderboard</button>
      <ul>
        {leaderboard.map((user, index) => (
          <li key={index}>
            {user.username}: {user[order]}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
