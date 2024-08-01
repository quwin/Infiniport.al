import React, { useState, useEffect, useRef } from 'react';
import axios from "axios";
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';

function SearchBar() {
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

        const exactMatch = searchData.find(item => item.username === input);

        if (exactMatch) {
          window.location.href = `/player/${exactMatch._id}`;
        } else {
          const mappedUsernames = searchData.map(item => item.username);
          const mappedIDs = searchData.map(item => item._id);

          setSearchResult(mappedUsernames);
          setidResult(mappedIDs);
        }
      } else {
          console.error("Expected an array but got:", searchData);
      }
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
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
        padding: .4rem 1.2rem;
        font-size: 1rem;
      } 
      `}
      </style>
      <Row className="justify-content-center">
        <Col xs="auto" style={{position: 'relative', minWidth: '15rem', width: '17rem'}}>
          <ListGroup 
            defaultActiveKey="0" 
            style={{ position: 'absolute', padding: 0,   width: '100%',  maxHeight: '100%', zIndex: 2 }}
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
                href={`/player/${idResult[index]}`}
              >
                  {player}
                </ListGroup.Item>
              ))}
          </ListGroup>
        </Col>
        <Col xs="auto" style={{paddingLeft: '1rem'}}>
          <button 
            style={{border: 0, }}
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
      </>
    );
}

export default SearchBar;