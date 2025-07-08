import React, { useState, useEffect } from 'react';
import './InventoryManager.css';

/**
 * InventoryManager component - A responsive inventory management interface
 * for tracking product stock levels, managing inventory, and handling alerts
 */
const InventoryManager = () => {
  // Inventory state
  const [inventory, setInventory] = useState([]);
  const [filteredInventory, setFilteredInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter and sort state
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [stockFilter, setStockFilter] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  
  // Stock update state
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);
  const [updateQuantity, setUpdateQuantity] = useState('');
  const [updateType, setUpdateType] = useState('add');
  const [updateReason, setUpdateReason] = useState('');
  const [submitting, setSubmitting] = useState(false);
  
  // Alert thresholds
  const [lowStockThreshold, setLowStockThreshold] = useState(10);
  const [criticalStockThreshold, setCriticalStockThreshold] = useState(5);
  
  // Message state
  const [message, setMessage] = useState({ type: null, text: null });
  
  // Categories list
  const categories = [
    'Electronics',
    'Clothing',
    'Home & Kitchen',
    'Books',
    'Toys',
    'Beauty',
    'Sports',
    'Automotive',
    'Health',
    'Other'
  ];
  
  // Stock adjustment reasons
  const stockReasons = [
    'New Stock',
    'Returned Items',
    'Damaged Items',
    'Inventory Count',
    'Theft/Loss',
    'Promotional Giveaway',
    'Vendor Return',
    'Quality Control',
    'Other'
  ];
  
  // Fetch inventory on component mount
  useEffect(() => {
    fetchInventory();
  }, []);
  
  // Apply filters and sorting when inventory or filter criteria change
  useEffect(() => {
    filterAndSortInventory();
  }, [inventory, searchQuery, categoryFilter, stockFilter, sortBy, sortOrder]);
  
  // Fetch inventory from API
  const fetchInventory = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Simulate API call with sample data
      setTimeout(() => {
        const sampleInventory = [
          {
            id: '1',
            sku: 'WH-001',
            name: 'Wireless Headphones',
            category: 'Electronics',
            quantity: 45,
            reorderPoint: 15,
            optimalStock: 60,
            unitCost: 50.00,
            totalValue: 2250.00,
            location: 'Warehouse A, Shelf 3',
            lastUpdated: '2023-06-20T14:45:00Z',
            status: 'In Stock'
          },
          {
            id: '2',
            sku: 'CTS-100',
            name: 'Cotton T-Shirt',
            category: 'Clothing',
            quantity: 120,
            reorderPoint: 30,
            optimalStock: 150,
            unitCost: 8.50,
            totalValue: 1020.00,
            location: 'Warehouse B, Shelf 1',
            lastUpdated: '2023-04-10T09:15:00Z',
            status: 'In Stock'
          },
          {
            id: '3',
            sku: 'CM-200',
            name: 'Coffee Maker',
            category: 'Home & Kitchen',
            quantity: 30,
            reorderPoint: 10,
            optimalStock: 40,
            unitCost: 75.00,
            totalValue: 2250.00,
            location: 'Warehouse A, Shelf 5',
            lastUpdated: '2023-05-18T16:30:00Z',
            status: 'In Stock'
          },
          {
            id: '4',
            sku: 'YM-300',
            name: 'Yoga Mat',
            category: 'Sports',
            quantity: 75,
            reorderPoint: 20,
            optimalStock: 100,
            unitCost: 15.00,
            totalValue: 1125.00,
            location: 'Warehouse C, Shelf 2',
            lastUpdated: '2023-02-14T13:45:00Z',
            status: 'In Stock'
          },
          {
            id: '5',
            sku: 'SC-400',
            name: 'Smartphone Case',
            category: 'Electronics',
            quantity: 200,
            reorderPoint: 50,
            optimalStock: 250,
            unitCost: 5.00,
            totalValue: 1000.00,
            location: 'Warehouse A, Shelf 1',
            lastUpdated: '2023-04-05T09:30:00Z',
            status: 'In Stock'
          },
          {
            id: '6',
            sku: 'DL-500',
            name: 'Desk Lamp',
            category: 'Home & Kitchen',
            quantity: 0,
            reorderPoint: 15,
            optimalStock: 30,
            unitCost: 20.00,
            totalValue: 0.00,
            location: 'Warehouse B, Shelf 4',
            lastUpdated: '2023-06-01T11:10:00Z',
            status: 'Out of Stock'
          },
          {
            id: '7',
            sku: 'WJ-600',
            name: 'Winter Jacket',
            category: 'Clothing',
            quantity: 25,
            reorderPoint: 20,
            optimalStock: 50,
            unitCost: 60.00,
            totalValue: 1500.00,
            location: 'Warehouse C, Shelf 3',
            lastUpdated: '2023-05-25T10:45:00Z',
            status: 'In Stock'
          },
          {
            id: '8',
            sku: 'BS-700',
            name: 'Bluetooth Speaker',
            category: 'Electronics',
            quantity: 60,
            reorderPoint: 20,
            optimalStock: 80,
            unitCost: 35.00,
            totalValue: 2100.00,
            location: 'Warehouse A, Shelf 2',
            lastUpdated: '2023-03-15T13:20:00Z',
            status: 'In Stock'
          },
          {
            id: '9',
            sku: 'FT-800',
            name: 'Fitness Tracker',
            category: 'Electronics',
            quantity: 5,
            reorderPoint: 10,
            optimalStock: 30,
            unitCost: 40.00,
            totalValue: 200.00,
            location: 'Warehouse A, Shelf 4',
            lastUpdated: '2023-06-10T16:40:00Z',
            status: 'Low Stock'
          },
          {
            id: '10',
            sku: 'CB-900',
            name: 'Cutting Board',
            category: 'Home & Kitchen',
            quantity: 40,
            reorderPoint: 15,
            optimalStock: 50,
            unitCost: 12.00,
            totalValue: 480.00,
            location: 'Warehouse B, Shelf 2',
            lastUpdated: '2023-02-28T14:15:00Z',
            status: 'In Stock'
          },
          {
            id: '11',
            sku: 'DP-999',
            name: 'Discontinued Product',
            category: 'Other',
            quantity: 3,
            reorderPoint: 0,
            optimalStock: 0,
            unitCost: 20.00,
            totalValue: 60.00,
            location: 'Warehouse D, Clearance',
            lastUpdated: '2023-01-15T11:30:00Z',
            status: 'Discontinued'
          },
          {
            id: '12',
            sku: 'BP-101',
            name: 'Backpack',
            category: 'Clothing',
            quantity: 2,
            reorderPoint: 10,
            optimalStock: 30,
            unitCost: 45.00,
            totalValue: 90.00,
            location: 'Warehouse C, Shelf 1',
            lastUpdated: '2023-06-15T10:20:00Z',
            status: 'Critical Stock'
          }
        ];
        
        setInventory(sampleInventory);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('Failed to fetch inventory. Please try again.');
      setLoading(false);
    }
  };
  
  // Filter and sort inventory based on current criteria
  const filterAndSortInventory = () => {
    let filtered = [...inventory];
    
    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(item => 
        item.name.toLowerCase().includes(query) ||
        item.sku.toLowerCase().includes(query) ||
        item.location.toLowerCase().includes(query)
      );
    }
    
    // Apply category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(item => item.category === categoryFilter);
    }
    
    // Apply stock filter
    if (stockFilter !== 'all') {
      filtered = filtered.filter(item => item.status === stockFilter);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
      let valueA = a[sortBy];
      let valueB = b[sortBy];
      
      // Handle special cases for sorting
      if (sortBy === 'quantity' || sortBy === 'unitCost' || sortBy === 'totalValue' || sortBy === 'reorderPoint') {
        valueA = Number(valueA) || 0;
        valueB = Number(valueB) || 0;
      } else {
        valueA = String(valueA || '').toLowerCase();
        valueB = String(valueB || '').toLowerCase();
      }
      
      if (sortOrder === 'asc') {
        return valueA > valueB ? 1 : -1;
      } else {
        return valueA < valueB ? 1 : -1;
      }
    });
    
    setFilteredInventory(filtered);
  };
  
  // Open stock update modal
  const openUpdateModal = (item) => {
    setCurrentItem(item);
    setUpdateQuantity('');
    setUpdateType('add');
    setUpdateReason('');
    setShowUpdateModal(true);
  };
  
  // Close stock update modal
  const closeUpdateModal = () => {
    setShowUpdateModal(false);
    setCurrentItem(null);
    setUpdateQuantity('');
    setUpdateType('add');
    setUpdateReason('');
  };
  
  // Handle stock update
  const handleStockUpdate = (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    // Validate form
    if (!updateQuantity || !updateReason) {
      setMessage({ type: 'error', text: 'Please fill in all required fields.' });
      setSubmitting(false);
      return;
    }
    
    const quantity = parseInt(updateQuantity, 10);
    if (isNaN(quantity) || quantity <= 0) {
      setMessage({ type: 'error', text: 'Please enter a valid quantity.' });
      setSubmitting(false);
      return;
    }
    
    // Simulate API call
    setTimeout(() => {
      const updatedInventory = inventory.map(item => {
        if (item.id === currentItem.id) {
          const newQuantity = updateType === 'add' 
            ? item.quantity + quantity 
            : Math.max(0, item.quantity - quantity);
          
          let newStatus = 'In Stock';
          if (newQuantity === 0) {
            newStatus = 'Out of Stock';
          } else if (newQuantity <= criticalStockThreshold) {
            newStatus = 'Critical Stock';
          } else if (newQuantity <= lowStockThreshold) {
            newStatus = 'Low Stock';
          } else if (item.status === 'Discontinued') {
            newStatus = 'Discontinued';
          }
          
          return {
            ...item,
            quantity: newQuantity,
            totalValue: parseFloat((newQuantity * item.unitCost).toFixed(2)),
            lastUpdated: new Date().toISOString(),
            status: newStatus
          };
        }
        return item;
      });
      
      setInventory(updatedInventory);
      setMessage({ 
        type: 'success', 
        text: `Successfully ${updateType === 'add' ? 'added' : 'removed'} ${quantity} units of ${currentItem.name}.` 
      });
      
      setSubmitting(false);
      closeUpdateModal();
      
      // Clear message after 3 seconds
      setTimeout(() => {
        setMessage({ type: null, text: null });
      }, 3000);
    }, 1500);
  };
  
  // Get current inventory items for pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredInventory.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredInventory.length / itemsPerPage);
  
  // Change page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  
  // Format currency
  const formatCurrency = (value) => {
    if (!value && value !== 0) return '';
    return `$${Number(value).toFixed(2)}`;
  };
  
  // Get stock status badge class
  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'In Stock': return 'status-in-stock';
      case 'Low Stock': return 'status-low-stock';
      case 'Critical Stock': return 'status-critical-stock';
      case 'Out of Stock': return 'status-out-of-stock';
      case 'Discontinued': return 'status-discontinued';
      default: return '';
    }
  };
  
  // Calculate inventory statistics
  const calculateStats = () => {
    if (!inventory.length) return { totalItems: 0, totalValue: 0, lowStockItems: 0, outOfStockItems: 0 };
    
    return {
      totalItems: inventory.reduce((sum, item) => sum + item.quantity, 0),
      totalValue: inventory.reduce((sum, item) => sum + item.totalValue, 0).toFixed(2),
      lowStockItems: inventory.filter(item => item.status === 'Low Stock' || item.status === 'Critical Stock').length,
      outOfStockItems: inventory.filter(item => item.status === 'Out of Stock').length
    };
  };
  
  const stats = calculateStats();
  
  return (
    <div className="inventory-manager">
      <div className="inventory-manager-header">
        <h2>Inventory Management</h2>
        <div className="threshold-controls">
          <div className="threshold-control">
            <label htmlFor="low-stock-threshold">Low Stock Threshold:</label>
            <input 
              type="number" 
              id="low-stock-threshold" 
              value={lowStockThreshold}
              onChange={(e) => setLowStockThreshold(parseInt(e.target.value, 10) || 0)}
              min="1"
            />
          </div>
          <div className="threshold-control">
            <label htmlFor="critical-stock-threshold">Critical Stock Threshold:</label>
            <input 
              type="number" 
              id="critical-stock-threshold" 
              value={criticalStockThreshold}
              onChange={(e) => setCriticalStockThreshold(parseInt(e.target.value, 10) || 0)}
              min="1"
            />
          </div>
        </div>
      </div>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.type === 'success' ? (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          )}
          <span>{message.text}</span>
        </div>
      )}
      
      {/* Inventory Statistics */}
      <div className="inventory-stats">
        <div className="stat-card">
          <div className="stat-value">{stats.totalItems}</div>
          <div className="stat-label">Total Items</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${stats.totalValue}</div>
          <div className="stat-label">Total Value</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.lowStockItems}</div>
          <div className="stat-label">Low Stock Items</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.outOfStockItems}</div>
          <div className="stat-label">Out of Stock</div>
        </div>
      </div>
      
      {/* Filters and Search */}
      <div className="filters-container">
        <div className="search-container">
          <input 
            type="text" 
            placeholder="Search inventory..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="search-icon">
            <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
          </svg>
        </div>
        
        <div className="filter-group">
          <select 
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
          
          <select 
            value={stockFilter}
            onChange={(e) => setStockFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Stock Status</option>
            <option value="In Stock">In Stock</option>
            <option value="Low Stock">Low Stock</option>
            <option value="Critical Stock">Critical Stock</option>
            <option value="Out of Stock">Out of Stock</option>
            <option value="Discontinued">Discontinued</option>
          </select>
        </div>
        
        <div className="sort-group">
          <select 
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="name">Name</option>
            <option value="sku">SKU</option>
            <option value="quantity">Quantity</option>
            <option value="category">Category</option>
            <option value="totalValue">Total Value</option>
            <option value="lastUpdated">Last Updated</option>
          </select>
          
          <button 
            className="sort-direction-button"
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            aria-label={sortOrder === 'asc' ? 'Sort descending' : 'Sort ascending'}
          >
            {sortOrder === 'asc' ? (
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
            )}
          </button>
        </div>
      </div>
      
      {/* Inventory Table */}
      <div className="inventory-table-container">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading inventory...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p>{error}</p>
            <button onClick={fetchInventory} className="retry-button">
              Retry
            </button>
          </div>
        ) : filteredInventory.length === 0 ? (
          <div className="empty-container">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clipRule="evenodd" />
            </svg>
            <p>No inventory items found. Try adjusting your filters.</p>
          </div>
        ) : (
          <>
            <table className="inventory-table">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Product</th>
                  <th>Category</th>
                  <th>Quantity</th>
                  <th>Status</th>
                  <th>Location</th>
                  <th>Unit Cost</th>
                  <th>Total Value</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentItems.map(item => (
                  <tr key={item.id} className={item.quantity <= item.reorderPoint ? 'reorder-row' : ''}>
                    <td>{item.sku}</td>
                    <td>{item.name}</td>
                    <td>{item.category}</td>
                    <td className="quantity-cell">
                      <div className="quantity-display">
                        <span className="quantity-value">{item.quantity}</span>
                        {item.quantity <= item.reorderPoint && (
                          <span className="reorder-indicator" title={`Reorder Point: ${item.reorderPoint}`}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </span>
                        )}
                      </div>
                      <div className="stock-bar-container">
                        <div 
                          className={`stock-bar ${getStockBarClass(item.quantity, item.optimalStock)}`}
                          style={{ width: `${Math.min(100, (item.quantity / item.optimalStock) * 100)}%` }}
                        ></div>
                      </div>
                    </td>
                    <td>
                      <span className={`status-badge ${getStatusBadgeClass(item.status)}`}>
                        {item.status}
                      </span>
                    </td>
                    <td>{item.location}</td>
                    <td>{formatCurrency(item.unitCost)}</td>
                    <td>{formatCurrency(item.totalValue)}</td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="update-button" 
                          onClick={() => openUpdateModal(item)}
                          aria-label="Update stock"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            {/* Pagination */}
            {totalPages > 1 && (
              <div className="pagination">
                <button 
                  onClick={() => paginate(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="pagination-button"
                  aria-label="Previous page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                
                <div className="pagination-pages">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(number => (
                    <button
                      key={number}
                      onClick={() => paginate(number)}
                      className={`pagination-number ${currentPage === number ? 'active' : ''}`}
                    >
                      {number}
                    </button>
                  ))}
                </div>
                
                <button 
                  onClick={() => paginate(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="pagination-button"
                  aria-label="Next page"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            )}
          </>
        )}
      </div>
      
      {/* Stock Update Modal */}
      {showUpdateModal && currentItem && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Update Stock: {currentItem.name}</h3>
              <button 
                className="close-modal-button" 
                onClick={closeUpdateModal}
                aria-label="Close modal"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            
            <div className="modal-body">
              <div className="item-details">
                <div className="detail-row">
                  <span className="detail-label">SKU:</span>
                  <span className="detail-value">{currentItem.sku}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Current Quantity:</span>
                  <span className="detail-value">{currentItem.quantity}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Status:</span>
                  <span className={`status-badge ${getStatusBadgeClass(currentItem.status)}`}>
                    {currentItem.status}
                  </span>
                </div>
              </div>
              
              <form onSubmit={handleStockUpdate} className="update-form">
                <div className="form-group">
                  <label htmlFor="update-type">Action:</label>
                  <div className="radio-group">
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="update-type" 
                        value="add" 
                        checked={updateType === 'add'}
                        onChange={() => setUpdateType('add')}
                      />
                      Add Stock
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="update-type" 
                        value="remove" 
                        checked={updateType === 'remove'}
                        onChange={() => setUpdateType('remove')}
                      />
                      Remove Stock
                    </label>
                  </div>
                </div>
                
                <div className="form-group">
                  <label htmlFor="update-quantity">Quantity: <span className="required">*</span></label>
                  <input 
                    type="number" 
                    id="update-quantity" 
                    value={updateQuantity}
                    onChange={(e) => setUpdateQuantity(e.target.value)}
                    min="1"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="update-reason">Reason: <span className="required">*</span></label>
                  <select 
                    id="update-reason" 
                    value={updateReason}
                    onChange={(e) => setUpdateReason(e.target.value)}
                    required
                  >
                    <option value="">Select Reason</option>
                    {stockReasons.map(reason => (
                      <option key={reason} value={reason}>{reason}</option>
                    ))}
                  </select>
                </div>
                
                <div className="form-actions">
                  <button 
                    type="button" 
                    className="cancel-button"
                    onClick={closeUpdateModal}
                    disabled={submitting}
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="save-button"
                    disabled={submitting}
                  >
                    {submitting ? (
                      <>
                        <span className="spinner"></span>
                        <span>Updating...</span>
                      </>
                    ) : 'Update Stock'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to determine stock bar class based on quantity
const getStockBarClass = (quantity, optimalStock) => {
  const percentage = (quantity / optimalStock) * 100;
  
  if (percentage === 0) return 'empty';
  if (percentage <= 15) return 'critical';
  if (percentage <= 30) return 'low';
  if (percentage > 100) return 'overstock';
  return 'normal';
};

export default InventoryManager;