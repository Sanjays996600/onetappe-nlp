import React, { useEffect, useState } from 'react';
import axios from 'axios';

function BookingList() {
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get('/api/bookings', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setBookings(response.data);
      } catch (err) {
        setError('Failed to fetch bookings');
      }
    };
    fetchBookings();
  }, []);

  return (
    <div className="container mt-5">
      <h2>Booking List</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Buyer</th>
            <th>Seller</th>
            <th>Slot</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {bookings.map((booking) => (
            <tr key={booking.id}>
              <td>{booking.buyer}</td>
              <td>{booking.seller_id}</td>
              <td>{booking.slot}</td>
              <td>{booking.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BookingList;