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
import searchPlayer from './Search'
import logo from './logo.png';


function HeaderBar() {
  const [input, setInput] = useState("");
  const [searchResult, setSearchResult] = useState([]);
  const typingTimeout = useRef(null);
  useEffect(() => {
    if (typingTimeout.current) {
      clearTimeout(typingTimeout.current);
    }

    typingTimeout.current = setTimeout(async () => {
      if (input) {
        const result = await searchPlayer(input);
        setSearchResult(result);
      }
    }, 1000);

    return () => {
      if (typingTimeout.current) {
        clearTimeout(typingTimeout.current);
      }
    };
  }, [input]);

  const handleChange = (event) => {
    setInput(event.target.value);
  };

  
  const [isMobile, setIsMobile] = useState(window.innerWidth < 996);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 996);
    }

    window.addEventListener('resize', handleResize);

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

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
        padding: .2rem 1.1rem;
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
                alt="Infiniport.al Logo"
              />
              {' '}Infiniport.al
            </Navbar.Brand>
              <Nav className="me-auto">
              <Row>
              <Col>
                <Nav.Link href="about">About</Nav.Link>
              </Col>
              <Col>
                <NavDropdown data-bs-theme="light" title="Discord App" id="basic-nav-dropdown">
                  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.2">Terms of Conditions</NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.3">Privacy Policy</NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                </NavDropdown>
                </Col>
                </Row>
              </Nav>
            {isMobile ? (
            <>
              <Navbar.Toggle aria-controls="basic-navbar-nav" /> 
                <Navbar.Collapse id="basic-navbar-nav">
                  <Stack direction="horizontal">
                    <Stack direction="vertical">
                      <InputGroup>
                        {input.length > 0 && (
                          <DropdownButton
                            title=""
                            data-bs-theme="dark"
                            show={true}
                            style={{ position: "absolute", width: "100%", top: "100%", zIndex: 1000 }}
                          >
                            {searchResult.map((player, index) => (
                              <Dropdown.Item key={player._id} eventKey={player.username}>
                                {player.username}
                              </Dropdown.Item>
                            ))}
                          </DropdownButton>
                        )}
                        <Form>
                          <Form.Control
                            data-bs-theme="dark"
                            placeholder="Username/Wallet"
                            aria-label="Search"
                            value={input}
                            onChange={handleChange}
                          />
                         </Form>
                        </InputGroup>
                    </Stack>
                    <Button variant="outline-light" size="xxl" type="submit">Lookup</Button>
                  </Stack>
              </Navbar.Collapse>
            </>
          ) : (
            <>
              <Stack direction="horizontal">
                <Stack direction="vertical">
                  <InputGroup>
                    {input.length > 0 && (
                      <DropdownButton
                        title=""
                        data-bs-theme="dark"
                        show={true}
                        style={{ position: "absolute", width: "100%", top: "100%", zIndex: 1000 }}
                      >
                        {searchResult.map((player, index) => (
                          <Dropdown.Item key={player._id} eventKey={player.username}>
                            {player.username}
                          </Dropdown.Item>
                        ))}
                      </DropdownButton>
                    )}
                    <Form>
                      <Form.Control
                        data-bs-theme="dark"
                        placeholder="Search by Username/Wallet"
                        aria-label="Search"
                        value={input}
                        onChange={handleChange}
                      />
                     </Form>
                    </InputGroup>
                </Stack>
                <Button variant="outline-light" size="xxl" type="submit">Lookup</Button>
              </Stack>
            </>
          )}
        </Container>
      </Navbar>
      </>
    );
}

export default HeaderBar;