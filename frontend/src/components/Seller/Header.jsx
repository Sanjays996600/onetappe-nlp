import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <header>
      <h1>Welcome Seller</h1>
      <button onClick={handleLogout}>Logout</button>
    </header>
  );
};

export default Header;