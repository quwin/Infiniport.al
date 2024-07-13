import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl'
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import logo from './logo.png';


function HeaderBar() {
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
                <Col xs={8}>
                  <Form className="d-flex">
                    <Form.Control
                      data-bs-theme="light"
                      placeholder="Username/Wallet/UserID"
                      aria-label="Search"
                      aria-describedby="basic-addon1"
                    />
                    <Button variant="infini" size="xxl" type="submit">Lookup</Button>
                  </Form>
                </Col>
              </Navbar.Collapse>
            </>
          ) : (
            <>
              <Col xs={4}>
                 <InputGroup>
                  <InputGroup.Text data-bs-theme="dark" id="basic-addon1">Find Profile:</InputGroup.Text>
                  <Form.Control
                    data-bs-theme="dark"
                    placeholder="Search by Username/Wallet/PlayerID"
                    aria-label="Search"
                    aria-describedby="basic-addon1"
                  />
                </InputGroup>
              </Col>
              <Col xs="auto">
                <Button variant="outline-light" size="xxl" type="submit">Lookup</Button>
              </Col>
            </>
          )}
        </Container>
      </Navbar>
      </>
    );
}

export default HeaderBar;