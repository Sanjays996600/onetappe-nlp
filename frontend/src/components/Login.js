import React, { useState } from 'react';
import axios from 'axios';

function Login() {
  const [token, setToken] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Example API call to validate token
      const response = await axios.post('/api/login', { token });
      if (response.data.success) {
        // Save token and redirect to bookings
        localStorage.setItem('authToken', token);
        window.location.href = '/bookings';
      } else {
        setError('Invalid token');
      }
    } catch (err) {
      setError('Login failed');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Seller Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="token" className="form-label">Token</label>
          <input
            type="text"
            className="form-control"
            id="token"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            required
          />
        </div>
        {error && <div className="alert alert-danger">{error}</div>}
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
    </div>
  );
}

export default Login;