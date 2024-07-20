import React, { useState, useEffect, useRef } from 'react';
import axios from "axios";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl'
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button'
import Stack from "react-bootstrap/Stack";
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import Spinner from 'react-bootstrap/Spinner';
import ListGroup from 'react-bootstrap/ListGroup';
import logo from './logo.png';

function HeaderBar() {
  const [isNavCollapsed, setIsNavCollapsed] = useState(true);
  const [input, setInput] = useState("");
  const [searchResult, setSearchResult] = useState([]);
  const [idResult, setidResult] = useState([]);
  const buttonRef = useRef(null);
  const resultsRef = useRef(null);

  const handleNavCollapse = async () => {
    setIsNavCollapsed(false);
    if (input.length > 0) {
      try {
        fetchSearch()
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
      }
    }
  }

  const handleChange = (event) => {
    setInput(event.target.value);

    if (event.target.value.length === 0) {
      setSearchResult([]);
      setidResult([]);
      setIsNavCollapsed(true);
    } 
  };

  const fetchSearch = async () => {
    let url = `/search/${input}`;

    try {
      const response = await axios.get(url);

      const searchData = Array.isArray(response.data) ? response.data : [response.data];

      if (Array.isArray(searchData)) {

          const mappedUsernames = searchData.map(item => (item.username));
          const mappedIDs = searchData.map(item => (item._id));

          setSearchResult(mappedUsernames);
          setidResult(mappedIDs);
      } else {
          console.error("Expected an array but got:", searchData);
      }
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  };

  const handleItemClick = (player, index) => {
    alert(`You clicked on ${player} on index ${index} with id ${idResult[index]}`);
  };

  const handleClickOutside = (event) => {
    if (
        (buttonRef.current && buttonRef.current.contains(event.target)) ||
        (resultsRef.current && resultsRef.current.contains(event.target))
      ) {
        return;
      } else {
        setSearchResult([]);
        setidResult([]);
        setIsNavCollapsed(true);
      }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent form submission
      handleNavCollapse();
    }
  };

  return ( /*purple = 712cf9 */

    <>
      <style type="text/css">
        {`    
      .btn-infini {
        background-color: #ec424c !important;
        color: white !important;
        border-radius: 6px;
      }

      .btn-infini:hover {
        background-color: #b42a4c !important;  
      }

      .btn-xxl {
        padding: .5rem 1.2rem;
        font-size: 1rem;
      } 
      .navbar-infini {
        background-color: #18141a !important;
        color: black !important;
        border-bottom: 1px solid !important;
        border-color: #b42a4c !important
      }

      .navbar-infini .navbar-brand {
        color: white !important;
      }

      .navbar-infini .navbar-toggler,
      .navbar-infini .nav-link {
        color: #8c8a8d !important;
      }
      `}
      </style>
       <Navbar variant="infini" expand="lg" fixed="top">
          <Container>
            <Navbar.Brand href="#home">
              <img
                src={logo}
                width="30"
                height="30"
                className="d-inline-block align-top"
                alt="Logo"
              />
              {' '}Infiniport.al
            </Navbar.Brand>
            <Nav className="me-auto">
            <Row>
            <Col>
              <Nav.Link href="about">About</Nav.Link>
            </Col>
            <Col>
              <NavDropdown data-bs-theme="dark" title="Discord App" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">Terms of Conditions</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">Privacy Policy</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
              </NavDropdown>
            </Col>
            </Row>
          </Nav>
        <>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">            <Stack direction="horizontal" gap={3} style={{position: 'relative', padding: 0, width: '100%'}}>

              <Container fluid>
                <Row>
                  <Col sm={4}/>
                  <Col sm={5} style={{position: 'relative'}}>
                    <ListGroup 
                      defaultActiveKey="#1" 
                      style={{ position: 'absolute', padding: 0,  width: '100%',  maxHeight: '100%'}}
                       ref={resultsRef}
                    >
                      <Form style={{ padding: 0, width: '100%'}}>
                        <Form.Control
                          data-bs-theme="dark"
                          type="search"
                          placeholder="Enter Username/Wallet Address"
                          className="me-2"
                          aria-label="Search"
                          onChange={handleChange}
                          onKeyPress={handleKeyPress}
                        />
                      </Form>
                      {!isNavCollapsed && searchResult.map((player, index) => (
                         <ListGroup.Item 
                          key={index}
                          style={{width: '100%'}}
                          action 
                          variant="dark" 
                          data-bs-theme="dark"
                          onClick={() => handleItemClick(player, index)}
                        >
                            {player}
                          </ListGroup.Item>
                        ))}
                    </ListGroup>
                  </Col>
                  <Col>
                    <button 
                      style={{border: 0}}
                      class="btn-infini btn-xxl"
                      type="button" 
                      data-toggle="collapse" 
                      data-target="#searchResults" 
                      aria-controls="searchResults" 
                      aria-expanded={!isNavCollapsed ? true : false} 
                      aria-label="Toggle navigation" 
                      onClick={handleNavCollapse}
                      ref={buttonRef}
                    >
                      Search
                    </button>
                  </Col>
                </Row>
              </Container>
            </Stack>
          </Navbar.Collapse>
        </>
        </Container>
      </Navbar>
      </>
    );
}

export default HeaderBar;