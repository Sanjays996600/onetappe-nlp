import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await axios.get('/orders');
        setOrders(res.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching orders", error);
        setError("Failed to load orders. Please try again.");
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  if (loading) return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h3 className="text-lg font-bold mb-4">Order Management</h3>
            <p>Loading orders...</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );

  if (error) return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h3 className="text-lg font-bold mb-4">Order Management</h3>
            <p className="text-red-500">{error}</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );

  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h3 className="text-lg font-bold mb-4">Order Management</h3>
            
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white">
                <thead>
                  <tr>
                    <th className="py-2 px-4 bg-gray-200">Order ID</th>
                    <th className="py-2 px-4 bg-gray-200">Product</th>
                    <th className="py-2 px-4 bg-gray-200">Quantity</th>
                    <th className="py-2 px-4 bg-gray-200">Date</th>
                    <th className="py-2 px-4 bg-gray-200">Status</th>
                    <th className="py-2 px-4 bg-gray-200">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.length > 0 ? (
                    orders.map((order, index) => (
                      <tr 
                        key={index} 
                        className={`border-b ${order.status === 'Pending' ? 'bg-yellow-50' : ''}`}
                      >
                        <td className="py-2 px-4">{order.id}</td>
                        <td className="py-2 px-4">{order.product}</td>
                        <td className="py-2 px-4">{order.quantity}</td>
                        <td className="py-2 px-4">{new Date(order.date).toLocaleDateString()}</td>
                        <td className="py-2 px-4">
                          <span 
                            className={`px-2 py-1 rounded text-xs ${order.status === 'Completed' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-yellow-100 text-yellow-800'}`}
                          >
                            {order.status}
                          </span>
                        </td>
                        <td className="py-2 px-4">
                          <Link 
                            to={`/invoice/${order.id}`}
                            className="bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded text-xs"
                          >
                            Generate Invoice
                          </Link>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="py-4 text-center">No orders found</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Orders;