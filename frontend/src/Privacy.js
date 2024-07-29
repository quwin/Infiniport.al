import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Stack from "react-bootstrap/Stack";
import "bootstrap/dist/css/bootstrap.min.css";

function Privacy() {
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
          <Row className="justify-content-center">
            <Col xs="auto">
              <h1>Privacy Policy</h1>
              <br/>
              This Privacy Policy describes how Infiniport.al collects, uses, and discloses information when you use Infiniport.al ("the Bot") and ("the Website)". <br/>
              <br/>
              <h4>Information We Collect:</h4>
              <h6> User Data:</h6>
              When you interact with the Bot, we may collect information such as your Discord user ID, username, linked Pixels.xyz Accounts, and messages sent to the Bot. <br/><br/>
              <h6> Discord Server Data:</h6>
              We may collect information about the servers in which the Bot is installed, including server ID and server settings. <br/>
              <br/>
              <h6> Pixels Player Data: </h6>
              We may collect information from the Pixels.xyz API when you search for information on that user via the Bot or the Website, and use that to populate our Leaderboards <br/>
               <br/>
              <h4>How We Use Your Information: </h4>
              <h6>To Provide and Maintain the Service:</h6>
               We use the collected data to operate and maintain the Bot and the Websitee. <br/><br/>
              <h6> To Communicate with You:</h6>
               We may use your information to respond to your inquiries and provide support. <br/>
               <br/>
              <h6> Data Security</h6>
              We implement a variety of security measures to maintain the safety of your information. However, no method of transmission over the Internet or electronic storage is 100% secure. <br/>
               <br/>
               <h6>Changes to This Privacy Policy: </h6>
              We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy here. Your continued use of the Bot/Website after any changes constitutes your acceptance of the new Privacy Policy. <br/>
               <br/>
              Contact Us: <br/>
              If you have any questions about these Terms, please contact me (quwin) via DM on Discord.
            </Col>
          </Row>
        </Stack>
      </Container>
    </>
  );
}

export default Privacy;