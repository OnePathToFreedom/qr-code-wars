import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';

// Компоненты
import NavBar from './components/NavBar';
import HomePage from './pages/HomePage';
import PhrasePage from './pages/PhrasePage';
import MapPage from './pages/MapPage';
import LeaderboardPage from './pages/LeaderboardPage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ScannerPage from './pages/ScannerPage';

function App() {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // Проверяем, есть ли сохраненный токен авторизации
    const token = localStorage.getItem('token');
    if (token) {
      // В реальном приложении здесь нужно проверить токен на сервере
      const userData = JSON.parse(localStorage.getItem('user') || '{}');
      setUser(userData);
    }
  }, []);
  
  // Функция для авторизации пользователя
  const login = (userData, token) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };
  
  // Функция для выхода из аккаунта
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };
  
  return (
    <div className="App">
      <NavBar user={user} logout={logout} />
      <Container className="mt-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/phrase/:hash" element={<PhrasePage user={user} />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
          <Route
            path="/profile"
            element={user ? <ProfilePage user={user} /> : <Navigate to="/login" />}
          />
          <Route path="/scanner" element={<ScannerPage user={user} />} />
          <Route path="/login" element={<LoginPage login={login} />} />
          <Route path="/register" element={<RegisterPage login={login} />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App; 