import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Stack from "react-bootstrap/Stack";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Image from 'react-bootstrap/Image';
import Pagination from 'react-bootstrap/Pagination';
import "bootstrap/dist/css/bootstrap.min.css";

function Leaderboard() {
  const [tableName, setTableName] = useState("total");
  const [order, setOrder] = useState("level");
  const [serverId, setServerId] = useState("");
  const [pageNumber, setPageNumber] = useState('1');
  const [quantity, setQuantity] = useState('15');
  const [leaderboard, setLeaderboard] = useState([]);
  let active = 1;
  let items = [];
  for (let number = 1; number <= 10; number++) {
    items.push(
      <Pagination.Item 
        key={number} 
        active={number === active}
        onClick={() => { setPageNumber(number.toString());
                         active = number;
        }}
      >
        {number}
      </Pagination.Item>,
    );
  }

  const SKILLS = [
    "forestry",
    "woodwork",
    "farming",
    "cooking",
    "mining",
    "metalworking",
    "stoneshaping",
    "business",
    "petcare",
    "exploration",
  ];

  useEffect(() => {
    fetchLeaderboard();
  }, [tableName, order, pageNumber, quantity, serverId]);

  const fetchLeaderboard = async () => {
    let url = `/leaderboard/${tableName}/${order}/${pageNumber}/${quantity}`;
    if (serverId) {
      url += `/${serverId}`;
    }

    try {
      const response = await axios.get(url);
      setLeaderboard(response.data);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  };

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

        .form-label {
          flex-shrink: 0;
          overflow: hidden;
        }

        .list-group-dark .list-group-item {
          background-color: #242129;
          color: #ffffff;
          border-color: #141418;
        }

        .table-borderless
        .table-borderless td,     
        .table-borderless th,
        .table-borderless tr,
        .table-borderless {
            border: 0;
            padding: 3px;
            background-color: #18141a;
        }

        ::-webkit-scrollbar {
          height: 8px !important;
          width: 6px !important;
          color: #18141a;
        }
        
        ::-webkit-scrollbar-track {
          background: #18141a; 
        }
         
        ::-webkit-scrollbar-thumb {
          background: #242129; 
          border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
          background: #b42a4c; 
        }

        .table-lb td,     
        .table-lb th,
        .table-lb tr {
            color: #cbd5e1;
            border: 1px dashed ;
            border-color: #829499;
            padding: 4px;
            background-color: #242129;
        }


        .stack-main {
            background-color: #18141a !important;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            padding: 10px;
            border: 1px solid transparent;
        }

        .btn-xxl {
          padding: .5rem 1.2rem;
          font-size: 1rem;
          border: 0;
        }

        .btn-infini {
          background-color: #ec424c !important;
          color: white !important;
          border-radius: 6px;
        }

        .btn-infini:hover {
          background-color: #b42a4c !important;  
        }

       .img-sm {
          height: 20px;
          width: 20px;
        } 

        .btn-lg {
          height: 3rem;
          padding: .1rem 2.5rem;
          font-size: .8rem;
        }

        .no-padding {
        padding: 0
        }

        .btn-outline-primary-red {
          color: #dc5d5d !important;
          background-color: #242129 !important;
        }

        .btn-outline-primary-red:hover {
          color: white !important;
          background-color: #ec424c !important;
        }
        `}
      </style>
      <Container>
        <Stack gap={3} direction="horizontal">
          <span style={{ width: 75}}>
            <svg class="MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-vubbuv" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="LeaderboardIcon">
            <path d="M7.5 21H2V9h5.5v12zm7.25-18h-5.5v18h5.5V3zM22 11h-5.5v10H22V11z"></path>
            </svg>
          </span>
          <Row>
            <Col>
              <h2>Pixels Leaderboard</h2>
              <h9>
                Complete skill ranking of all players in Pixels
              </h9>
            </Col>
          </Row>
        </Stack>
        <Row>
          <Col>
          <br/>
            <Stack gap={1} direction="vertical" className="stack-main">
              <Form>
                <Stack direction="horizontal">
                  <Form.Group sm={{span: 4}} as={Col} controlId="formUsernameLb">
                    <Form.Label className="form-label">Find Player</Form.Label>  
                    <Form.Control data-bs-theme="dark" type="username" placeholder="Enter Username"/>
                  </Form.Group>
                  <Form.Group sm={{ span: 7, offset: 1}} as={Col} controlId="formGuild">
                    <Form.Label>Search Guild</Form.Label>
                    <Form.Control data-bs-theme="dark" type="guild" placeholder="Enter Guild Handle" onChange={(e) => setServerId(e.target.value.toLowerCase())}/>
                  </Form.Group>
                </Stack>
              </Form>
              <Form>
                <Stack direction="horizontal">
                  <Col span="3">
                    <div>Sort by</div>
                       <ButtonGroup aria-label="exp">
                          <Button 
                            variant='infini'
                            size='xxl'
                            class="btn-infini btn-xxl"
                            onClick={() => setOrder("level")}
                          >
                            Level
                          </Button>
                          <Button 
                            variant='infini'
                            size='xxl'
                            class="btn-infini btn-xxl"
                            onClick={() => setOrder("exp")}
                          >
                            Exp
                          </Button>
                        </ButtonGroup>
                  </Col>
                  <Form.Group sm={{span: 2}} as={Col} controlId="selectRows">
                    <FloatingLabel className="form-label" data-bs-theme="dark" label="Rows:" >
                      <Form.Select 
                        aria-label="Floating label rows shown"
                        value={quantity}
                        onChange={e => {
                          setQuantity(e.target.value);
                        }}
                      >
                        <option value="15">15</option>
                        <option value="30">30</option>
                        <option value="50">50</option>
                      </Form.Select>
                    </FloatingLabel>
                  </Form.Group>
                </Stack>
                <Form.Check sm={{ span: 2, offset: 11}} data-bs-theme="dark"  type="switch" id="custom-switch" label="Endless Scrolling"/>
              </Form>
              <Container className="no-padding">
                <Table className="table-borderless" responsive>
                  <thead>
                    <tr>
                      <th>
                        <Button
                          size="xxl"
                          variant="outline-primary-red"
                          onClick={() => setTableName("total")}
                        >
                          Overall
                        </Button>{" "}
                      </th>
                      {SKILLS.map((skill) => (
                        <th key={skill}>
                          <Button
                            size="lg"
                            variant="outline-primary-red"
                            onClick={() => setTableName(skill)}>
                              <Stack direction="vertical">
                                <Container>
                                  <Image
                                    src={`https://d31ss916pli4td.cloudfront.net/game/ui/skills/skills_icon_${skill}.png`}
                                    className="img-sm"
                                    fluid
                                    alt={`${skill} icon`}
                                  />
                                </Container>
                                <span lassName="form-label">{skill.charAt(0).toUpperCase() + skill.slice(1)}</span>
                              </Stack>
                          </Button>
                        </th>
                      ))}
                    </tr>
                  </thead>
                </Table>
              </Container>
              <ul className="list-group list-group-dark">
              <Table variant="lb" responsive>
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Username</th>
                    <th>Level</th>
                    <th style={{textAlign: 'right'}}>Exp</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((user, index) => (
                    <tr>
                      <th key={index}> #{index+((pageNumber-1)*quantity) + 1} </th>
                      <th key={index}>
                        <a href={`/player/${user.user_id}`}>{user.username}</a>
                      </th>
                      <th key={index}> {user.level} </th>
                      <th key={index} style={{textAlign: 'right'}}> {user.exp.toLocaleString('en-US', { maximumFractionDigits: 0 })}</th>
                    </tr>
                  ))}
                </tbody>
              </Table>
              </ul>
              <Row className="justify-content-center">
                <Col xs="auto">
                  <Pagination data-bs-theme="dark">{items}</Pagination>
                </Col>
              </Row>
            </Stack>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default Leaderboard;