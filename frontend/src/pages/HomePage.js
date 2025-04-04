import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <Container>
      <Row className="mb-5">
        <Col>
          <div className="text-center py-5">
            <h1 className="display-4 mb-4">QR Code Wars</h1>
            <p className="lead">
              Собирайте мотивационные фразы на немецком языке, сканируя QR-коды в городе.
              Соревнуйтесь с другими игроками и отслеживайте свой прогресс на карте!
            </p>
          </div>
        </Col>
      </Row>
      
      <Row className="mb-4">
        <Col md={4} className="mb-4">
          <Card className="h-100">
            <Card.Body>
              <Card.Title>Сканируйте QR-коды</Card.Title>
              <Card.Text>
                Ищите QR-коды в разных местах города. Каждый код содержит уникальную 
                мотивационную фразу на немецком языке, которую вы можете добавить в свою коллекцию.
              </Card.Text>
              <Link to="/scanner">
                <Button variant="primary">Открыть сканер</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4} className="mb-4">
          <Card className="h-100">
            <Card.Body>
              <Card.Title>Следите за картой</Card.Title>
              <Card.Text>
                Отслеживайте свой прогресс на интерактивной карте города. 
                Видите, какие места вы уже посетили и где еще стоит побывать.
              </Card.Text>
              <Link to="/map">
                <Button variant="primary">Открыть карту</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4} className="mb-4">
          <Card className="h-100">
            <Card.Body>
              <Card.Title>Соревнуйтесь</Card.Title>
              <Card.Text>
                Станьте лидером в нашем рейтинге! Соревнуйтесь с другими 
                участниками, собирая больше фраз и открывая новые места.
              </Card.Text>
              <Link to="/leaderboard">
                <Button variant="primary">Смотреть лидеров</Button>
              </Link>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <Row className="mt-5">
        <Col className="text-center">
          <h3>Новый QR-код появится через:</h3>
          <div className="display-4 mb-4">23:45:12</div>
          <p>Следите за обновлениями и не пропустите новые фразы!</p>
        </Col>
      </Row>
    </Container>
  );
};

export default HomePage; 