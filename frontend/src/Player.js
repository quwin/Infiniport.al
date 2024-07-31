import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import PlayerCard from './PlayerCard';
import SearchBar from './SearchBar';
import "bootstrap/dist/css/bootstrap.min.css";
import axios from 'axios';

function Player() {
  let { player_id } = useParams();

  const [skillData, setSkillData] = useState([
    ['Forestry'],
    ['Woodwork'],
    ['Farming'],
    ['Cooking'],
    ['Petcare'],
    ['Exploration'],
    ['Mining'],
    ['Stoneshaping'],
    ['Metalworking'],
    ['Business'],
  ]);
  const [coins, setCoins] = useState(0);
  const [pixel, setPixel] = useState(0);
  const [lands, setLands] = useState(0);
  const [username, setUsername] = useState('');
  const [rank, setRank] = useState(0);
  const [profileImg, setProfileImg] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchPlayer = async () => {
    let url = `/player_data/${player_id}`;
    let rank_url = `/player_rank/${player_id}`;
    
    try {
      const dataResponse = await axios.get(url);
      const rankResponse = await axios.get(rank_url);
      const playerData = dataResponse.data;
      const rankData = rankResponse.data;

      const updatedSkillData = skillData.map(skill => {
        const skillKey = skill[0].toLowerCase();
        return playerData.levels[skillKey] 
          ? [skill[0], playerData.levels[skillKey].level, playerData.levels[skillKey].totalExp] 
          : [skill[0], 0, 0]
      });

      setSkillData(updatedSkillData);
      setUsername(playerData.username);
      setRank(rankData.rank)
      setLands(playerData.memberships["nftLand-pixels"] ? playerData.memberships["nftLand-pixels"].count : 0);
      setProfileImg((playerData.currentAvatar["pieces"] && playerData.currentAvatar["pieces"]["image"]) ? playerData.currentAvatar["pieces"]["image"] : "")
      setLoading(false);
      setCoins(playerData.coinInventory[8].balance);
      setPixel(playerData.coinInventory[1].balance);
    } catch (error) {
      console.error(`Error fetching player ${player_id}:`, error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlayer();
  }, [player_id]);

  return (
    <>
      <style type="text/css">
      {`    
        body {
          background-color: #242129 !important;
          color: white;
          margin: 0;
          padding: 0;
          height: 100vh;
          width: 100vw;
        }
      `}
      </style>
      <Container>
        <div style={{ height: '2vh' }} />
        <Row className="justify-content-center">
          <Col xs="auto">
            {loading || username == '' ? (
              <SearchBar/>
            ) : (
              <PlayerCard
                skillData={skillData}
                coins={coins}
                pixel={pixel}
                lands={lands}
                username={username}
                userID={player_id}
                profileImg={profileImg}
                rank={rank}
                footer={<SearchBar/>}
              />
            )}
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default Player;
