import React, { useState, useEffect } from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import { Link } from 'react-router-dom';
import './dashboard.css';

/**
 * DashboardHome component for displaying the main dashboard landing page
 * This component provides a responsive overview of key metrics and quick access to main features
 */
const DashboardHome = () => {
  const [stats, setStats] = useState({
    totalSales: 0,
    totalOrders: 0,
    pendingOrders: 0,
    lowStockItems: 0
  });
  
  const [recentOrders, setRecentOrders] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Fetch dashboard data
  useEffect(() => {
    setIsLoading(true);
    
    // Simulate API call with setTimeout
    setTimeout(() => {
      // Sample data - in a real app, this would come from an API
      setStats({
        totalSales: 12580,
        totalOrders: 156,
        pendingOrders: 23,
        lowStockItems: 8
      });
      
      setRecentOrders([
        { id: 'ORD-1234', customer: 'John Doe', date: '2023-06-15', total: 120.50, status: 'Completed' },
        { id: 'ORD-1235', customer: 'Sarah Smith', date: '2023-06-14', total: 85.25, status: 'Processing' },
        { id: 'ORD-1236', customer: 'Robert Johnson', date: '2023-06-14', total: 210.75, status: 'Completed' },
        { id: 'ORD-1237', customer: 'Emily Wilson', date: '2023-06-13', total: 45.99, status: 'Completed' },
        { id: 'ORD-1238', customer: 'Michael Brown', date: '2023-06-12', total: 150.00, status: 'Pending' }
      ]);
      
      setTopProducts([
        { id: 1, name: 'Premium T-Shirt', sold: 245, revenue: 4900 },
        { id: 2, name: 'Designer Jeans', sold: 187, revenue: 7480 },
        { id: 3, name: 'Leather Wallet', sold: 156, revenue: 3120 },
        { id: 4, name: 'Wireless Earbuds', sold: 134, revenue: 6700 }
      ]);
      
      setIsLoading(false);
    }, 800);
    
    // In a real application, you would fetch from an API:
    // Promise.all([
    //   fetch('/api/dashboard/stats').then(res => res.json()),
    //   fetch('/api/dashboard/recent-orders').then(res => res.json()),
    //   fetch('/api/dashboard/top-products').then(res => res.json())
    // ])
    //   .then(([statsData, ordersData, productsData]) => {
    //     setStats(statsData);
    //     setRecentOrders(ordersData);
    //     setTopProducts(productsData);
    //     setIsLoading(false);
    //   })
    //   .catch(err => {
    //     console.error('Error fetching dashboard data:', err);
    //     setIsLoading(false);
    //   });
  }, []);
  
  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };
  
  // Get status color class
  const getStatusColorClass = (status) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
            </div>
          ) : (
            <div className="p-4">
              <h2 className="text-xl font-bold mb-6">Dashboard Overview</h2>
              
              {/* Stats Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-teal-500">
                  <div className="text-gray-500 text-sm font-medium">Total Sales</div>
                  <div className="text-2xl font-bold text-gray-800">{formatCurrency(stats.totalSales)}</div>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-blue-500">
                  <div className="text-gray-500 text-sm font-medium">Total Orders</div>
                  <div className="text-2xl font-bold text-gray-800">{stats.totalOrders}</div>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-yellow-500">
                  <div className="text-gray-500 text-sm font-medium">Pending Orders</div>
                  <div className="text-2xl font-bold text-gray-800">{stats.pendingOrders}</div>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-red-500">
                  <div className="text-gray-500 text-sm font-medium">Low Stock Items</div>
                  <div className="text-2xl font-bold text-gray-800">{stats.lowStockItems}</div>
                </div>
              </div>
              
              {/* Quick Actions */}
              <div className="bg-white p-6 rounded-lg shadow-sm mb-8">
                <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Link to="/seller-dashboard/add-product" className="flex flex-col items-center justify-center p-4 bg-teal-50 rounded-lg hover:bg-teal-100 transition-colors">
                    <svg className="w-8 h-8 text-teal-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                    </svg>
                    <span className="text-sm font-medium text-gray-700">Add Product</span>
                  </Link>
                  
                  <Link to="/seller-dashboard/orders" className="flex flex-col items-center justify-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
                    <svg className="w-8 h-8 text-blue-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                    <span className="text-sm font-medium text-gray-700">View Orders</span>
                  </Link>
                  
                  <Link to="/seller-dashboard/analytics" className="flex flex-col items-center justify-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
                    <svg className="w-8 h-8 text-purple-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                    <span className="text-sm font-medium text-gray-700">Sales Analytics</span>
                  </Link>
                  
                  <Link to="/seller-dashboard/reports" className="flex flex-col items-center justify-center p-4 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors">
                    <svg className="w-8 h-8 text-yellow-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <span className="text-sm font-medium text-gray-700">Generate Reports</span>
                  </Link>
                </div>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent Orders */}
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-semibold">Recent Orders</h3>
                    <Link to="/seller-dashboard/orders" className="text-sm text-teal-600 hover:text-teal-800">View All</Link>
                  </div>
                  
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead>
                        <tr className="border-b">
                          <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
                          <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                          <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                          <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recentOrders.map((order, index) => (
                          <tr key={index} className="border-b hover:bg-gray-50">
                            <td className="py-3 px-3 text-sm font-medium text-gray-900">{order.id}</td>
                            <td className="py-3 px-3 text-sm text-gray-500">{order.customer}</td>
                            <td className="py-3 px-3 text-sm text-gray-500">{formatCurrency(order.total)}</td>
                            <td className="py-3 px-3 text-sm">
                              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColorClass(order.status)}`}>
                                {order.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
                
                {/* Top Products */}
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-semibold">Top Selling Products</h3>
                    <Link to="/seller-dashboard/products" className="text-sm text-teal-600 hover:text-teal-800">View All</Link>
                  </div>
                  
                  <div className="space-y-4">
                    {topProducts.map((product, index) => (
                      <div key={index} className="flex justify-between items-center border-b pb-3">
                        <div>
                          <div className="font-medium text-gray-800">{product.name}</div>
                          <div className="text-sm text-gray-500">{product.sold} units sold</div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold text-teal-600">{formatCurrency(product.revenue)}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DashboardHome;