import React from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Stack from "react-bootstrap/Stack";
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Image from 'react-bootstrap/Image'
import PlayerCard from './PlayerCard';
import SearchBar from './SearchBar';
import ColumnChart from './Column';
import logo from './images/pixelslogo.png';

import "bootstrap/dist/css/bootstrap.min.css";

function Home() {
  const testData = [
    ['Forestry', 43, 732284],
    ['Woodwork', 82, 39826591],
    ['Farming', 48, 1314934],
    ['Cooking', 41, 609120],
    ['Petcare', 8, 6245],
    ['Exploration', 1, 125],
    ['Mining', 24, 81620],
    ['Stoneshaping', 64, 6305573],
    ['Metalworking', 29, 161942],
    ['Business', 49, 1356430],
  ];
  
  const coins = 23165159;
  const pixel = 2042;
  const rep = 4063.21;
  const lands = 1;
  
  const profileImg = 'https://res.cloudinary.com/alchemyapi/image/upload/thumbnailv2/eth-mainnet/7ff6f0431edb8318d6fa91d9e520f564';
  const userID = '65e3dd3bebdfdac278077b85'
  
   /*#1e293b*/
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
      <Stack gap={3} className="mx-auto">
        <div style={{height: '1vh'}}/>
        <Row className="justify-content-center text-center">
          <Col xs="auto">
            <Image src={logo} style={{width: '8rem'}} />
            <br/>
            <h4> Community Leaderboard / Utilities</h4>
          </Col>
        </Row>
        <div style={{height: '1vh'}}/>
        <Row className="justify-content-center">
          <Col xs="auto">
            <PlayerCard
              skillData={testData}
              coins={coins}
              pixel={pixel}
              lands={lands}
              username={'Find your Profile'}
              userID={userID}
              profileImg={profileImg}
              footer={<SearchBar/>}
              interval={4000}
              rank='???'
            />
            <div style={{height: '2vh'}}/>
          </Col>
          <Col xs="auto">
            <Card style={{ minWidth: '25rem', maxWidth: '25rem', minHeight: '25rem', backgroundColor: '#18141a', border: "0", zIndex: 1 }}>
              <Card.Header as="h4" style={{ color: '#cbd5e1', backgroundColor: "#1b1b1d", padding: '.8rem', height: '3.5rem'}}>
                <Stack direction="horizontal" gap={3}>
                <span style={{maxWidth: '20rem'}}>View Leaderboards</span>
                </Stack>
              </Card.Header>
              <Card.Body style={{ width: '100%', height: '100%', padding: 0 }}>
                <ColumnChart/>
              </Card.Body>
              <Card.Footer className="text-muted" style={{ color: '#cbd5e1', backgroundColor: "#1b1b1d", padding: '.5rem', height: '3.5rem'}}>
                <Row className="justify-content-center" style={{paddingLeft: '.8rem', paddingRight: '.8rem'}}>
                  <Button href="/leaderboard" variant="info">Lets Go!</Button>
                </Row>
              </Card.Footer>
            </Card>
            <div style={{height: '2vh'}}/>
          </Col>
          <Col xs="auto">
            <Card style={{ minWidth: '25rem', maxWidth: '25rem', minHeight: '25rem', backgroundColor: '#1e1f22', border: "0", zIndex: 1 }}>
              <Card.Body style={{ width: '100%', height: '100%', padding: 0 }}>
                <iframe src="https://discord.com/widget?id=1245569744476700733&theme=dark" width="400" height="450" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts">
                </iframe>
              </Card.Body>
              <Card.Footer style={{backgroundColor: "#1b1b1d", padding: '.5rem', height: '3.5rem'}}>
                <Row className="justify-content-center" style={{paddingLeft: '.8rem', paddingRight: '.8rem'}}>
                  <Button href="https://discord.com/oauth2/authorize?client_id=1233991850470277130&scope=bot&permissions=1342598160" variant="primary">Add to Server</Button>
                </Row>
              </Card.Footer>
            </Card>
            <div style={{height: '2vh'}}/>
          </Col>
        </Row>
      </Stack>
      </Container>
    </>
  );
}

export default Home;