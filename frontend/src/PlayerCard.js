import React from "react";
import Table from "react-bootstrap/Table";
import Stack from "react-bootstrap/Stack";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Image from 'react-bootstrap/Image';
import RadarChart from './Radar';
import PolarChart from './Polar';
import Carousel from 'react-bootstrap/Carousel';
import Card from 'react-bootstrap/Card';
import "bootstrap/dist/css/bootstrap.min.css";

const PlayerCard = ({ 
  skillData,
  coins,
  pixel,
  rep,
  lands,
  username,
  userID,
  profileImg,
  rank,
  footer = null,
  interval = null
  
}) => {
  const totalExp = skillData.reduce((sum, row) => sum + row[2], 0);
  const totalLvl = skillData.reduce((sum, row) => sum + row[1], 0);

  const coinImg = 'https://d31ss916pli4td.cloudfront.net/uploadedAssets/currency/cur_coins/e66e4f48-2b99-45f8-b8fc-74d43e391d1c.png';
  const pixelImg = 'https://d31ss916pli4td.cloudfront.net/uploadedAssets/currency/pixels_pixel_currency_new_2.png';
  const iconLink= 'https://d31ss916pli4td.cloudfront.net/game/ui/skills/skills_icon_'
  const landImg = 'https://play.pixels.xyz/favicon/favicon.ico'

   /*#1e293b*/
  return (
    <>
      <style type="text/css">
          {`    
          .div-sm {
            padding: .4rem .4rem;
            border-radius: .8rem;
            font-size: .9rem;
          } 
          .carousel-inner,
          carousel-inner {
            padding: 0;
            min-height: 25rem;
          }

          .carousel slide,
          carousel slide {
            padding: 0;
            min-height: 25rem;
          }

          .anychart-credits,
          anychart-credits {
            display: none;
            pointer-events: none;
          }

          .table-borderless
          .table-borderless td,     
          .table-borderless th,
          .table-borderless tr,
          .table-borderless {
            border: 0;
            padding: 0;
            padding-right: 1.1rem;
            padding-left: 1.5rem;
            background-color: #18141a;
            font-size: .9rem;
            color: #94a3b8;
          }
          `}
      </style>
        <Card style={{ minWidth: '25rem', maxWidth: '25rem', minHeight: '25rem', backgroundColor: '#18141a', border: "0" }}>
        <Card.Header as="h4" style={{ color: '#cbd5e1', backgroundColor: "#1b1b1d", padding: '.8rem', height: '3.5rem'}}>
          <Stack direction="horizontal" gap={3}>
          <span style={{maxWidth: '14rem'}}>{username}</span>
          <div class="div-sm" style={{ backgroundColor: "#323234"}}> Rank #{rank} </div>
          <Image rounded style={{width: "2rem"}} src={profileImg}/>
          </Stack>
        </Card.Header>
        <Card.Body style={{ width: '100%', height: '100%', padding: 0 }}>
          <Carousel 
            interval={interval}
            controls={false}
            indicators={true}
            touch={true} 
            keyboard={true} 
            style={{ width: '100%', minHeight: '25rem', padding: 0 }}
          >
            <Carousel.Item style={{ padding: 0, height: "100%" }}>
              <Stack gap={4} direction="vertical">
                <Row style={{ minWidth: '100%', height: '2rem', color: '#94a3b8', fontSize: '.9rem'}}>
                  <Col style={{ padding: '1rem', paddingLeft: '2rem', paddingRight: '0'}}>
                    {userID}
                    <br/>
                    Reputation: <span  style={{color: "#cbd5e1" }}>
                     {rep.toLocaleString('en-US', { maximumFractionDigits: 2 })}
                    </span>
                  </Col>
                  <Col style={{ padding: '1rem', paddingRight: '2rem', paddingleft: '0', textAlign: 'right'}}>
                    <span  style={{color: "#cbd5e1" }}>
                      <Image style={{width: "1rem"}} src={coinImg}/> {coins.toLocaleString('en-US')}
                    </span>
                    <br/>
                    <span style={{color: "#cbd5e1" }}>
                      <Image style={{width: "1rem"}} src={pixelImg}/> {pixel.toLocaleString('en-US', { maximumFractionDigits: 1 })}
                    </span>
                    <br/>
                    <span style={{color: "#cbd5e1" }}>
                      <Image style={{width: "1rem"}} src={landImg}/> {lands}
                    </span>
                  </Col>
                </Row>
                <Row style={{ minWidth: '100%', height: '3rem', color: '#94a3b8', fontSize: '.9rem'}}>
                  <Col style={{ padding: '1rem', paddingLeft: '2rem', paddingRight: '0'}}>
                    Player Stats:
                    <br/>
                    Total Lvl: <span  style={{color: "#cbd5e1" }}>
                     Lvl {totalLvl.toLocaleString('en-US', { maximumFractionDigits: 0 })}
                    </span>
                  </Col>
                  <Col style={{ padding: '1rem', paddingRight: '2rem', paddingleft: '0', textAlign: 'right'}}>
                    <br/>
                    Total Exp: <span  style={{color: "#cbd5e1", textAlign: 'right' }}>
                     {totalExp.toLocaleString('en-US', { maximumFractionDigits: 0 })} xp
                    </span>
                  </Col>
                </Row>
                <Table variant="borderless" style={{ padding: 0, height: "100%", width: '100%' }} responsive>
                  <thead>
                    <tr>
                      <th>Skill</th>
                      <th>Level</th>
                      <th style={{textAlign: 'right'}}>Exp</th>
                    </tr>
                  </thead>
                  <tbody>
                    {skillData.map((data, index) => (
                      <tr>
                        <th key={data}>
                          <Image 
                            style={{width: "1rem"}} 
                            src={iconLink + data[0].toLowerCase() + '.png'}
                          /> {data[0]} 
                         </th>
                        <th style={{color: "#cbd5e1" }}> Lvl {data[1]} </th>
                        <th style={{color: "#cbd5e1", textAlign: 'right'}}> {data[2].toLocaleString('en-US', { maximumFractionDigits: 0 })}  xp</th>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Stack>
            </Carousel.Item>
            <Carousel.Item style={{ padding: 0, minHeight: '25rem' }}>
              <PolarChart skillData={skillData} />
            </Carousel.Item>
          </Carousel>
        </Card.Body>
        {footer && (<Card.Footer className="text-muted" style={{ color: '#cbd5e1', backgroundColor: "#1b1b1d", padding: '.5rem', height: '3.5rem'}} className="text-muted">{footer}</Card.Footer>)}
      </Card>
    </>
  );
}

export default PlayerCard;