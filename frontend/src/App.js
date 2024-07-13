import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import "./App.css";

function App() {
  const [tableName, setTableName] = useState("total");
  const [order, setOrder] = useState("level");
  const [serverId, setServerId] = useState("");
  const [leaderboard, setLeaderboard] = useState([]);
  const SKILLS = [
    "forestry",
    "woodwork",
    "cooking",
    "mining",
    "exploration",
    "farming",
    "stoneshaping",
    "petcare",
    "business",
    "metalworking",
  ];

  useEffect(() => {
    fetchLeaderboard();
  }, [tableName, order, serverId]); // Ensure fetchLeaderboard is called whenever these states change

  const fetchLeaderboard = async () => {
    let url = `/leaderboard/${tableName}/${order}/1`;
    if (serverId) {
      url += `/${serverId}`;
    }

    try {
      console.log(url);
      const response = await axios.get(url);
      setLeaderboard(response.data);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  };

  return (
    <>
    <style type="text/css">
      {`
    body {
      background-color: #18141a; /* Set the desired background color */
      margin: 0; /* Remove default margin */
      padding: 0; /* Remove default padding */
      height: 100vh; /* Ensure the body covers the full viewport height */
      width: 100vw; /* Ensure the body covers the full viewport width */
    }
    `}
    </style>
    <div className="App container">
      <h1 className="text-center my-4">Leaderboard</h1>
      <div className="form-group">
        <label htmlFor="tableName">Select Skill:</label>
        <select
          className="form-control"
          id="tableName"
          value={tableName}
          onChange={(e) => setTableName(e.target.value)}
        >
          <option value="total">Overall</option>
          {SKILLS.map((skill) => (
            <option key={skill} value={skill}>
              {skill.charAt(0).toUpperCase() + skill.slice(1)}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="order">Order By:</label>
        <select
          className="form-control"
          id="order"
          value={order}
          onChange={(e) => setOrder(e.target.value)}
        >
          <option value="level">Level</option>
          <option value="exp">Experience</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="serverId">Server ID (optional):</label>
        <input
          className="form-control"
          type="text"
          id="serverId"
          value={serverId}
          onChange={(e) => setServerId(e.target.value)}
          placeholder="Server ID (optional)"
        />
      </div>
      <Button
        className="btn btn-primary btn-primary-custom"
        onClick={fetchLeaderboard}
      >
        Get Leaderboard
      </Button>
      <ul className="list-group">
        {leaderboard.map((user, index) => (
          <li key={index} className="list-group-item">
            {user.username}: {user[order]}
          </li>
        ))}
      </ul>
    </div>
  </>
  );
}

export default App;
