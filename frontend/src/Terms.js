import React from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Stack from "react-bootstrap/Stack";
import "bootstrap/dist/css/bootstrap.min.css";

function Terms() {
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
              <h1>Terms of Service</h1>
              <br/>
              By using Infiniportal, you agree to comply with and be bound by these Terms of Service ("ToS"). If you do not agree to these terms, you must not use the Bot or Website. <br/>
              <br/>
              Infiniport.al provides Pixels.xyz player information to users on the Discord platform and this website (www.infiniport.al). The service is provided on an "as is" and "as available" basis. <br/><br/>
              You must not use Infiniport.al for any illegal or unauthorized purpose, including but not limited to cheating in Pixels.xyz. <br/>
              You must not, in the use of Infiniport.al, violate any laws in your jurisdiction. <br/>
              You must not abuse, harass, threaten, or intimidate other users of Infiniport.al or Pixels.xyz players. <br/>
              <br/>
              All content, trademarks, and data provided by Infiniport.al are the property of Infiniport.al or third parties. Unauthorized use of the Bot's content is prohibited. <br/>
               <br/>
              We reserve the right to modify or discontinue Infiniport.al at any time without notice. We also reserve the right to monetize any existing or new features at any time. <br/><br/>
              We reserve the right to terminate access to Infiniport.al immediately, without prior notice or liability, for any reason whatsoever, including if you breach the ToS. <br/>
               <br/>
              In no event shall we, nor our partners or affiliates, be liable for any damages, including without limitation, loss of profits, data, use, or other losses, resulting from <br/>
              (i) your use or inability to use the Bot; <br/>
              (ii) any unauthorized access to or use of our servers and/or any  information stored there. <br/>
               <br/>
              We reserve the right to modify these terms at any time. We will notify you of any changes by updating this page. Your continued use of Infiniport.al after any such changes constitutes your acceptance of the new ToS. <br/>
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

export default Terms;