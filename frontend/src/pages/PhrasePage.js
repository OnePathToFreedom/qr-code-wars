import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Alert } from 'react-bootstrap';
import axios from 'axios';

// Получаем API URL из переменных окружения или используем локальный URL для разработки
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const PhrasePage = ({ user }) => {
  const { hash } = useParams();
  const navigate = useNavigate();
  const [phrase, setPhrase] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [alreadyScanned, setAlreadyScanned] = useState(false);

  useEffect(() => {
    const fetchPhrase = async () => {
      try {
        const response = await axios.get(`${API_URL}/phrases/${hash}`);
        setPhrase(response.data);
        setLoading(false);
      } catch (err) {
        setError('Не удалось загрузить фразу. Возможно, QR-код недействителен.');
        setLoading(false);
      }
    };

    fetchPhrase();
  }, [hash]);

  const handleScan = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/users/scan/${hash}`,
        { user_agent: navigator.userAgent },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      
      if (response.data.message.includes('уже отсканировали')) {
        setAlreadyScanned(true);
      } else {
        setSuccess(true);
      }
    } catch (err) {
      setError('Не удалось сохранить сканирование. Попробуйте позже.');
    }
  };

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <Card className="phrase-card">
      <Card.Body className="text-center">
        <Card.Title className="mb-4">Мотивационная фраза</Card.Title>
        <Card.Text className="display-5 mb-4">"{phrase.text}"</Card.Text>
        
        {success && (
          <Alert variant="success">
            Отлично! Фраза добавлена в вашу коллекцию.
          </Alert>
        )}
        
        {alreadyScanned && (
          <Alert variant="info">
            Вы уже добавили эту фразу в свою коллекцию.
          </Alert>
        )}
        
        {!success && !alreadyScanned && (
          <Button 
            variant="primary" 
            size="lg" 
            onClick={handleScan}
            disabled={!user}
          >
            {user ? 'Добавить в коллекцию' : 'Войдите, чтобы сохранить'}
          </Button>
        )}
        
        {!user && !success && (
          <p className="mt-3">
            <Button variant="link" onClick={() => navigate('/login')}>
              Войти
            </Button> или 
            <Button variant="link" onClick={() => navigate('/register')}>
              Зарегистрироваться
            </Button>
          </p>
        )}
      </Card.Body>
    </Card>
  );
};

export default PhrasePage; 