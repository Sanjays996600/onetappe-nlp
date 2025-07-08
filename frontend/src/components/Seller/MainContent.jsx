import React, { useEffect, useState } from 'react';

const MainContent = () => {
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("access_token");
      const res = await fetch("http://localhost:8000/me", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const data = await res.json();
      setUser(data);
    };
    fetchUser();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("access_token");
      const headers = { Authorization: `Bearer ${token}` };

      const ordersRes = await fetch("http://localhost:8000/seller/orders", { headers });
      const ordersData = await ordersRes.json();
      setOrders(ordersData.orders);

      const inventoryRes = await fetch("http://localhost:8000/seller/inventory", { headers });
      const inventoryData = await inventoryRes.json();
      setInventory(inventoryData.inventory);
    };

    fetchData();
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h2>Welcome, {user.email}</h2>
      <p>Role: {user.role}</p>
      <div>
        <h3>Orders</h3>
        <ul>
          {orders.map((order, index) => (
            <li key={index}>{order}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Inventory</h3>
        <ul>
          {inventory.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default MainContent;