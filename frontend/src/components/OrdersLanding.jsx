import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './OrdersLanding.css';

/**
 * OrdersLanding component - A responsive landing page for managing customer orders
 * Features filtering, sorting, and detailed order information
 */
const OrdersLanding = () => {
  // State for orders data and UI controls
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date-desc');
  
  // Fetch orders data
  useEffect(() => {
    setIsLoading(true);
    setError(null);
    
    // Simulate API call with setTimeout
    setTimeout(() => {
      try {
        // Sample data - in a real app, this would come from an API
        const sampleOrders = [
          {
            id: 'ORD-1234',
            customer: {
              name: 'John Doe',
              email: 'john.doe@example.com',
              phone: '+1 (555) 123-4567'
            },
            date: '2023-06-15T14:30:00Z',
            total: 120.50,
            status: 'completed',
            items: [
              { id: 1, name: 'Premium T-Shirt', quantity: 2, price: 29.99 },
              { id: 2, name: 'Baseball Cap', quantity: 1, price: 19.99 },
              { id: 3, name: 'Sunglasses', quantity: 1, price: 39.99 }
            ],
            shipping: {
              address: '123 Main St, Anytown, CA 12345',
              method: 'Standard Shipping',
              cost: 5.99
            },
            payment: {
              method: 'Credit Card',
              last4: '4242'
            }
          },
          {
            id: 'ORD-1235',
            customer: {
              name: 'Sarah Smith',
              email: 'sarah.smith@example.com',
              phone: '+1 (555) 987-6543'
            },
            date: '2023-06-14T10:15:00Z',
            total: 85.25,
            status: 'processing',
            items: [
              { id: 4, name: 'Designer Jeans', quantity: 1, price: 79.99 },
              { id: 5, name: 'Socks', quantity: 1, price: 5.99 }
            ],
            shipping: {
              address: '456 Oak Ave, Springfield, IL 67890',
              method: 'Express Shipping',
              cost: 12.99
            },
            payment: {
              method: 'PayPal',
              email: 'sarah.smith@example.com'
            }
          },
          {
            id: 'ORD-1236',
            customer: {
              name: 'Robert Johnson',
              email: 'robert.johnson@example.com',
              phone: '+1 (555) 456-7890'
            },
            date: '2023-06-14T09:45:00Z',
            total: 210.75,
            status: 'completed',
            items: [
              { id: 6, name: 'Leather Jacket', quantity: 1, price: 199.99 },
              { id: 7, name: 'Leather Belt', quantity: 1, price: 29.99 }
            ],
            shipping: {
              address: '789 Pine St, Lakeside, NY 54321',
              method: 'Standard Shipping',
              cost: 5.99
            },
            payment: {
              method: 'Credit Card',
              last4: '1234'
            }
          },
          {
            id: 'ORD-1237',
            customer: {
              name: 'Emily Wilson',
              email: 'emily.wilson@example.com',
              phone: '+1 (555) 234-5678'
            },
            date: '2023-06-13T16:20:00Z',
            total: 45.99,
            status: 'completed',
            items: [
              { id: 8, name: 'Graphic T-Shirt', quantity: 1, price: 24.99 },
              { id: 9, name: 'Phone Case', quantity: 1, price: 14.99 },
              { id: 10, name: 'Stickers Pack', quantity: 1, price: 5.99 }
            ],
            shipping: {
              address: '321 Elm St, Rivertown, WA 13579',
              method: 'Standard Shipping',
              cost: 5.99
            },
            payment: {
              method: 'Apple Pay'
            }
          },
          {
            id: 'ORD-1238',
            customer: {
              name: 'Michael Brown',
              email: 'michael.brown@example.com',
              phone: '+1 (555) 876-5432'
            },
            date: '2023-06-12T11:05:00Z',
            total: 150.00,
            status: 'pending',
            items: [
              { id: 11, name: 'Wireless Earbuds', quantity: 1, price: 129.99 },
              { id: 12, name: 'Charging Cable', quantity: 2, price: 9.99 }
            ],
            shipping: {
              address: '654 Maple Ave, Hillcrest, TX 97531',
              method: 'Express Shipping',
              cost: 12.99
            },
            payment: {
              method: 'Credit Card',
              last4: '5678'
            }
          },
          {
            id: 'ORD-1239',
            customer: {
              name: 'Jessica Taylor',
              email: 'jessica.taylor@example.com',
              phone: '+1 (555) 345-6789'
            },
            date: '2023-06-11T14:50:00Z',
            total: 75.50,
            status: 'cancelled',
            items: [
              { id: 13, name: 'Summer Dress', quantity: 1, price: 59.99 },
              { id: 14, name: 'Sun Hat', quantity: 1, price: 24.99 }
            ],
            shipping: {
              address: '987 Cedar Rd, Beachside, FL 24680',
              method: 'Standard Shipping',
              cost: 5.99
            },
            payment: {
              method: 'Credit Card',
              last4: '9012'
            }
          },
          {
            id: 'ORD-1240',
            customer: {
              name: 'David Miller',
              email: 'david.miller@example.com',
              phone: '+1 (555) 567-8901'
            },
            date: '2023-06-10T09:30:00Z',
            total: 320.75,
            status: 'completed',
            items: [
              { id: 15, name: 'Smart Watch', quantity: 1, price: 299.99 },
              { id: 16, name: 'Watch Band', quantity: 1, price: 19.99 }
            ],
            shipping: {
              address: '246 Birch Ln, Mountain View, CA 86420',
              method: 'Express Shipping',
              cost: 12.99
            },
            payment: {
              method: 'Credit Card',
              last4: '3456'
            }
          }
        ];
        
        setOrders(sampleOrders);
        setFilteredOrders(sampleOrders);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to load orders. Please try again.');
        setIsLoading(false);
      }
    }, 800);
    
    // In a real application, you would fetch from an API:
    // fetch('/api/orders')
    //   .then(res => {
    //     if (!res.ok) throw new Error('Failed to fetch orders');
    //     return res.json();
    //   })
    //   .then(data => {
    //     setOrders(data);
    //     setFilteredOrders(data);
    //     setIsLoading(false);
    //   })
    //   .catch(err => {
    //     setError(err.message);
    //     setIsLoading(false);
    //   });
  }, []);
  
  // Apply filters and sorting whenever filter criteria or orders change
  useEffect(() => {
    if (!orders.length) return;
    
    let result = [...orders];
    
    // Apply status filter
    if (statusFilter !== 'all') {
      result = result.filter(order => order.status === statusFilter);
    }
    
    // Apply date filter
    if (dateFilter !== 'all') {
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      const lastWeek = new Date(today);
      lastWeek.setDate(lastWeek.getDate() - 7);
      const lastMonth = new Date(today);
      lastMonth.setMonth(lastMonth.getMonth() - 1);
      
      result = result.filter(order => {
        const orderDate = new Date(order.date);
        switch (dateFilter) {
          case 'today':
            return orderDate >= today;
          case 'yesterday':
            return orderDate >= yesterday && orderDate < today;
          case 'last-week':
            return orderDate >= lastWeek;
          case 'last-month':
            return orderDate >= lastMonth;
          default:
            return true;
        }
      });
    }
    
    // Apply search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(order => 
        order.id.toLowerCase().includes(query) ||
        order.customer.name.toLowerCase().includes(query) ||
        order.customer.email.toLowerCase().includes(query) ||
        order.items.some(item => item.name.toLowerCase().includes(query))
      );
    }
    
    // Apply sorting
    result.sort((a, b) => {
      switch (sortBy) {
        case 'date-desc':
          return new Date(b.date) - new Date(a.date);
        case 'date-asc':
          return new Date(a.date) - new Date(b.date);
        case 'total-desc':
          return b.total - a.total;
        case 'total-asc':
          return a.total - b.total;
        case 'id-asc':
          return a.id.localeCompare(b.id);
        case 'id-desc':
          return b.id.localeCompare(a.id);
        default:
          return 0;
      }
    });
    
    setFilteredOrders(result);
  }, [orders, statusFilter, dateFilter, searchQuery, sortBy]);
  
  // Format date
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };
  
  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };
  
  // Get status color class
  const getStatusColorClass = (status) => {
    switch (status) {
      case 'completed':
        return 'status-completed';
      case 'processing':
        return 'status-processing';
      case 'pending':
        return 'status-pending';
      case 'cancelled':
        return 'status-cancelled';
      default:
        return 'status-default';
    }
  };
  
  // Calculate order summary
  const getOrderSummary = () => {
    if (!orders.length) return { total: 0, completed: 0, processing: 0, pending: 0, cancelled: 0 };
    
    return orders.reduce((summary, order) => {
      summary.total += 1;
      summary[order.status] = (summary[order.status] || 0) + 1;
      return summary;
    }, { total: 0, completed: 0, processing: 0, pending: 0, cancelled: 0 });
  };
  
  const orderSummary = getOrderSummary();
  
  // Handle order action (in a real app, these would call API endpoints)
  const handleOrderAction = (orderId, action) => {
    console.log(`Performing ${action} on order ${orderId}`);
    // Here you would make API calls to update the order status
    // For demo purposes, we'll update the local state
    
    if (action === 'cancel') {
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, status: 'cancelled' } : order
      ));
    } else if (action === 'process') {
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, status: 'processing' } : order
      ));
    } else if (action === 'complete') {
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, status: 'completed' } : order
      ));
    }
  };
  
  return (
    <div className="orders-landing">
      {/* Order Summary */}
      <div className="order-summary">
        <div className="summary-card total">
          <h3>Total Orders</h3>
          <p className="count">{orderSummary.total}</p>
        </div>
        <div className="summary-card completed">
          <h3>Completed</h3>
          <p className="count">{orderSummary.completed}</p>
        </div>
        <div className="summary-card processing">
          <h3>Processing</h3>
          <p className="count">{orderSummary.processing}</p>
        </div>
        <div className="summary-card pending">
          <h3>Pending</h3>
          <p className="count">{orderSummary.pending}</p>
        </div>
        <div className="summary-card cancelled">
          <h3>Cancelled</h3>
          <p className="count">{orderSummary.cancelled}</p>
        </div>
      </div>
      
      {/* Filters and Controls */}
      <div className="orders-controls">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search orders by ID, customer, or product..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button className="search-button">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="search-icon">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
        
        <div className="filters">
          <div className="filter-group">
            <label htmlFor="status-filter">Status:</label>
            <select
              id="status-filter"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Statuses</option>
              <option value="completed">Completed</option>
              <option value="processing">Processing</option>
              <option value="pending">Pending</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="date-filter">Date:</label>
            <select
              id="date-filter"
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Time</option>
              <option value="today">Today</option>
              <option value="yesterday">Yesterday</option>
              <option value="last-week">Last 7 Days</option>
              <option value="last-month">Last 30 Days</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="sort-by">Sort By:</label>
            <select
              id="sort-by"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="filter-select"
            >
              <option value="date-desc">Date (Newest First)</option>
              <option value="date-asc">Date (Oldest First)</option>
              <option value="total-desc">Amount (High to Low)</option>
              <option value="total-asc">Amount (Low to High)</option>
              <option value="id-asc">Order ID (A-Z)</option>
              <option value="id-desc">Order ID (Z-A)</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Orders List */}
      {isLoading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading orders...</p>
        </div>
      ) : error ? (
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button className="retry-button" onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      ) : filteredOrders.length === 0 ? (
        <div className="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="empty-icon">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3>No orders found</h3>
          <p>Try adjusting your filters or search criteria</p>
        </div>
      ) : (
        <div className="orders-list">
          {filteredOrders.map((order) => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <div className="order-id">
                  <h3>{order.id}</h3>
                  <span className={`order-status ${getStatusColorClass(order.status)}`}>
                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                  </span>
                </div>
                <div className="order-date">
                  {formatDate(order.date)}
                </div>
              </div>
              
              <div className="order-customer">
                <div className="customer-info">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="customer-icon">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <div>
                    <p className="customer-name">{order.customer.name}</p>
                    <p className="customer-email">{order.customer.email}</p>
                  </div>
                </div>
                <div className="order-total">
                  <p className="total-label">Total</p>
                  <p className="total-amount">{formatCurrency(order.total)}</p>
                </div>
              </div>
              
              <div className="order-items">
                <h4>Items ({order.items.length})</h4>
                <ul className="items-list">
                  {order.items.map((item) => (
                    <li key={item.id} className="item">
                      <span className="item-name">{item.name}</span>
                      <span className="item-quantity">x{item.quantity}</span>
                      <span className="item-price">{formatCurrency(item.price)}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="order-shipping">
                <h4>Shipping</h4>
                <p className="shipping-address">{order.shipping.address}</p>
                <p className="shipping-method">{order.shipping.method} ({formatCurrency(order.shipping.cost)})</p>
              </div>
              
              <div className="order-actions">
                <Link to={`/invoice/${order.id}`} className="action-button invoice">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="action-icon">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Invoice
                </Link>
                
                {order.status === 'pending' && (
                  <button 
                    className="action-button process"
                    onClick={() => handleOrderAction(order.id, 'process')}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="action-icon">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Process
                  </button>
                )}
                
                {order.status === 'processing' && (
                  <button 
                    className="action-button complete"
                    onClick={() => handleOrderAction(order.id, 'complete')}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="action-icon">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Complete
                  </button>
                )}
                
                {(order.status === 'pending' || order.status === 'processing') && (
                  <button 
                    className="action-button cancel"
                    onClick={() => handleOrderAction(order.id, 'cancel')}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="action-icon">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default OrdersLanding;