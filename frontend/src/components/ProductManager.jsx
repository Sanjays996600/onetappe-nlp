import React, { useState, useEffect } from 'react';
import './ProductManager.css';

/**
 * ProductManager component - A responsive product management interface
 * for adding, editing, and managing products
 */
const ProductManager = () => {
  // Product list state
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Product form state
  const [showForm, setShowForm] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentProductId, setCurrentProductId] = useState(null);
  const [formSubmitting, setFormSubmitting] = useState(false);
  
  // Form data state
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    category: '',
    price: '',
    salePrice: '',
    cost: '',
    quantity: '',
    description: '',
    features: '',
    images: [],
    status: 'active'
  });
  
  // Filter and sort state
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [productsPerPage] = useState(10);
  
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
  
  // Fetch products on component mount
  useEffect(() => {
    fetchProducts();
  }, []);
  
  // Apply filters and sorting when products or filter criteria change
  useEffect(() => {
    filterAndSortProducts();
  }, [products, searchQuery, categoryFilter, statusFilter, sortBy, sortOrder]);
  
  // Fetch products from API
  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Simulate API call with sample data
      setTimeout(() => {
        const sampleProducts = [
          {
            id: '1',
            name: 'Wireless Headphones',
            sku: 'WH-001',
            category: 'Electronics',
            price: 99.99,
            salePrice: 79.99,
            cost: 50.00,
            quantity: 45,
            description: 'High-quality wireless headphones with noise cancellation.',
            features: 'Bluetooth 5.0, 30-hour battery life, Active Noise Cancellation',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2023-05-15T10:30:00Z',
            updatedAt: '2023-06-20T14:45:00Z'
          },
          {
            id: '2',
            name: 'Cotton T-Shirt',
            sku: 'CTS-100',
            category: 'Clothing',
            price: 24.99,
            salePrice: null,
            cost: 8.50,
            quantity: 120,
            description: 'Comfortable 100% cotton t-shirt.',
            features: 'Pre-shrunk, Machine washable, Available in multiple colors',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2023-04-10T09:15:00Z',
            updatedAt: '2023-04-10T09:15:00Z'
          },
          {
            id: '3',
            name: 'Coffee Maker',
            sku: 'CM-200',
            category: 'Home & Kitchen',
            price: 149.99,
            salePrice: 129.99,
            cost: 75.00,
            quantity: 30,
            description: 'Programmable coffee maker with thermal carafe.',
            features: '12-cup capacity, 24-hour programmability, Auto shut-off',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2023-03-22T11:20:00Z',
            updatedAt: '2023-05-18T16:30:00Z'
          },
          {
            id: '4',
            name: 'Yoga Mat',
            sku: 'YM-300',
            category: 'Sports',
            price: 35.99,
            salePrice: null,
            cost: 15.00,
            quantity: 75,
            description: 'Non-slip yoga mat for all types of yoga.',
            features: 'Eco-friendly material, 6mm thickness, Carrying strap included',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2023-02-14T13:45:00Z',
            updatedAt: '2023-02-14T13:45:00Z'
          },
          {
            id: '5',
            name: 'Smartphone Case',
            sku: 'SC-400',
            category: 'Electronics',
            price: 19.99,
            salePrice: 14.99,
            cost: 5.00,
            quantity: 200,
            description: 'Protective case for smartphones.',
            features: 'Shock-absorbent, Slim design, Multiple colors available',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2023-01-30T10:00:00Z',
            updatedAt: '2023-04-05T09:30:00Z'
          },
          {
            id: '6',
            name: 'Desk Lamp',
            sku: 'DL-500',
            category: 'Home & Kitchen',
            price: 45.99,
            salePrice: null,
            cost: 20.00,
            quantity: 0,
            description: 'Adjustable LED desk lamp with multiple brightness levels.',
            features: 'Touch control, USB charging port, Adjustable arm',
            images: ['https://via.placeholder.com/150'],
            status: 'out_of_stock',
            createdAt: '2022-12-15T15:20:00Z',
            updatedAt: '2023-06-01T11:10:00Z'
          },
          {
            id: '7',
            name: 'Winter Jacket',
            sku: 'WJ-600',
            category: 'Clothing',
            price: 129.99,
            salePrice: 99.99,
            cost: 60.00,
            quantity: 25,
            description: 'Warm winter jacket with water-resistant outer shell.',
            features: 'Insulated, Detachable hood, Multiple pockets',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2022-11-10T14:30:00Z',
            updatedAt: '2023-05-25T10:45:00Z'
          },
          {
            id: '8',
            name: 'Bluetooth Speaker',
            sku: 'BS-700',
            category: 'Electronics',
            price: 79.99,
            salePrice: 59.99,
            cost: 35.00,
            quantity: 60,
            description: 'Portable Bluetooth speaker with rich sound.',
            features: 'Waterproof, 12-hour battery life, Built-in microphone',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2022-10-05T09:45:00Z',
            updatedAt: '2023-03-15T13:20:00Z'
          },
          {
            id: '9',
            name: 'Fitness Tracker',
            sku: 'FT-800',
            category: 'Electronics',
            price: 89.99,
            salePrice: null,
            cost: 40.00,
            quantity: 5,
            description: 'Smart fitness tracker with heart rate monitoring.',
            features: 'Step counter, Sleep tracking, Smartphone notifications',
            images: ['https://via.placeholder.com/150'],
            status: 'low_stock',
            createdAt: '2022-09-20T11:15:00Z',
            updatedAt: '2023-06-10T16:40:00Z'
          },
          {
            id: '10',
            name: 'Cutting Board',
            sku: 'CB-900',
            category: 'Home & Kitchen',
            price: 29.99,
            salePrice: 24.99,
            cost: 12.00,
            quantity: 40,
            description: 'Bamboo cutting board with juice groove.',
            features: 'Eco-friendly, Non-slip feet, Reversible design',
            images: ['https://via.placeholder.com/150'],
            status: 'active',
            createdAt: '2022-08-15T10:30:00Z',
            updatedAt: '2023-02-28T14:15:00Z'
          },
          {
            id: '11',
            name: 'Discontinued Product',
            sku: 'DP-999',
            category: 'Other',
            price: 49.99,
            salePrice: null,
            cost: 20.00,
            quantity: 0,
            description: 'This product has been discontinued.',
            features: 'No longer available',
            images: ['https://via.placeholder.com/150'],
            status: 'discontinued',
            createdAt: '2022-07-10T09:00:00Z',
            updatedAt: '2023-01-15T11:30:00Z'
          }
        ];
        
        setProducts(sampleProducts);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('Failed to fetch products. Please try again.');
      setLoading(false);
    }
  };
  
  // Filter and sort products based on current criteria
  const filterAndSortProducts = () => {
    let filtered = [...products];
    
    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(product => 
        product.name.toLowerCase().includes(query) ||
        product.sku.toLowerCase().includes(query) ||
        product.description.toLowerCase().includes(query)
      );
    }
    
    // Apply category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(product => product.category === categoryFilter);
    }
    
    // Apply status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(product => product.status === statusFilter);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
      let valueA = a[sortBy];
      let valueB = b[sortBy];
      
      // Handle special cases for sorting
      if (sortBy === 'price' || sortBy === 'salePrice' || sortBy === 'cost' || sortBy === 'quantity') {
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
    
    setFilteredProducts(filtered);
  };
  
  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  // Handle image upload with improved error handling and Chrome-specific fixes
  const handleImageUpload = (e) => {
    try {
      const files = Array.from(e.target.files);
      
      if (files.length === 0) {
        return; // No files selected
      }
      
      // Validate file types and sizes
      const validFiles = files.filter(file => {
        // Check if file is an image
        if (!file.type.startsWith('image/')) {
          setMessage({ 
            type: 'error', 
            text: `"${file.name}" is not a valid image file. Please select only image files.` 
          });
          return false;
        }
        
        // Check file size (limit to 5MB)
        if (file.size > 5 * 1024 * 1024) {
          setMessage({ 
            type: 'error', 
            text: `"${file.name}" exceeds the 5MB size limit. Please compress the image or select a smaller file.` 
          });
          return false;
        }
        
        return true;
      });
      
      if (validFiles.length === 0) {
        return; // No valid files after filtering
      }
      
      // Create preview URLs for the selected images with retry mechanism
      const processFile = (file, retryCount = 0) => {
        try {
          // Create object URL for preview
          const preview = URL.createObjectURL(file);
          
          // Test the URL by creating a temporary image
          const testImage = new Image();
          
          return new Promise((resolve, reject) => {
            // Set up success handler
            testImage.onload = () => {
              resolve({
                file,
                preview,
                name: file.name
              });
            };
            
            // Set up error handler with retry logic
            testImage.onerror = () => {
              // Release the failed object URL
              URL.revokeObjectURL(preview);
              
              if (retryCount < 2) { // Allow up to 2 retries
                console.log(`Retrying image processing for ${file.name}, attempt ${retryCount + 1}`);
                // Wait a bit before retrying
                setTimeout(() => {
                  processFile(file, retryCount + 1)
                    .then(resolve)
                    .catch(reject);
                }, 500); // 500ms delay before retry
              } else {
                reject(new Error(`Failed to process image ${file.name} after multiple attempts`));
              }
            };
            
            // Start loading the image
            testImage.src = preview;
          });
        } catch (error) {
          return Promise.reject(error);
        }
      };
      
      // Process all valid files with the retry mechanism
      Promise.all(validFiles.map(file => processFile(file)))
        .then(newImages => {
          if (newImages.length > 0) {
            setFormData(prev => ({
              ...prev,
              images: [...prev.images, ...newImages]
            }));
            
            // Clear any error messages if successful
            if (message.type === 'error') {
              setMessage({ type: null, text: null });
            }
          }
        })
        .catch(error => {
          console.error('Image processing error:', error);
          setMessage({ 
            type: 'error', 
            text: 'Failed to process one or more images. Please try again or use a smaller image.' 
          });
        });
    } catch (error) {
      console.error('Image upload error:', error);
      setMessage({ 
        type: 'error', 
        text: 'Failed to upload images. Please try again or use a different browser if the problem persists.' 
      });
    }
  };
  
  // Remove image from form
  const handleRemoveImage = (index) => {
    setFormData(prev => {
      const updatedImages = [...prev.images];
      updatedImages.splice(index, 1);
      return { ...prev, images: updatedImages };
    });
  };
  
  // Open form to add new product
  const handleAddProduct = () => {
    setFormData({
      name: '',
      sku: '',
      category: '',
      price: '',
      salePrice: '',
      cost: '',
      quantity: '',
      description: '',
      features: '',
      images: [],
      status: 'active'
    });
    setEditMode(false);
    setCurrentProductId(null);
    setShowForm(true);
  };
  
  // Open form to edit existing product
  const handleEditProduct = (product) => {
    setFormData({
      name: product.name,
      sku: product.sku,
      category: product.category,
      price: product.price,
      salePrice: product.salePrice || '',
      cost: product.cost,
      quantity: product.quantity,
      description: product.description,
      features: product.features,
      images: product.images.map(img => ({ preview: img, name: img.split('/').pop() })),
      status: product.status
    });
    setEditMode(true);
    setCurrentProductId(product.id);
    setShowForm(true);
  };
  
  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setFormSubmitting(true);
    setMessage({ type: null, text: null });
    
    // Validate form
    if (!formData.name || !formData.sku || !formData.category || !formData.price) {
      setMessage({ type: 'error', text: 'Please fill in all required fields.' });
      setFormSubmitting(false);
      return;
    }
    
    // Simulate API call
    setTimeout(() => {
      if (editMode) {
        // Update existing product
        setProducts(prev => prev.map(product => 
          product.id === currentProductId ? { ...product, ...formData, updatedAt: new Date().toISOString() } : product
        ));
        setMessage({ type: 'success', text: 'Product updated successfully!' });
      } else {
        // Add new product
        const newProduct = {
          ...formData,
          id: String(Date.now()),
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        };
        setProducts(prev => [...prev, newProduct]);
        setMessage({ type: 'success', text: 'Product added successfully!' });
      }
      
      setFormSubmitting(false);
      
      // Clear form after successful submission
      setTimeout(() => {
        setShowForm(false);
        setMessage({ type: null, text: null });
      }, 2000);
    }, 1500);
  };
  
  // Handle product deletion
  const handleDeleteProduct = (productId) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      // Simulate API call
      setTimeout(() => {
        setProducts(prev => prev.filter(product => product.id !== productId));
        setMessage({ type: 'success', text: 'Product deleted successfully!' });
        
        // Clear message after 3 seconds
        setTimeout(() => {
          setMessage({ type: null, text: null });
        }, 3000);
      }, 1000);
    }
  };
  
  // Handle status change
  const handleStatusChange = (productId, newStatus) => {
    setProducts(prev => prev.map(product => 
      product.id === productId ? { ...product, status: newStatus, updatedAt: new Date().toISOString() } : product
    ));
  };
  
  // Get current products for pagination
  const indexOfLastProduct = currentPage * productsPerPage;
  const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
  const currentProducts = filteredProducts.slice(indexOfFirstProduct, indexOfLastProduct);
  const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
  
  // Change page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  
  // Format currency
  const formatCurrency = (value) => {
    if (!value && value !== 0) return '';
    return `$${Number(value).toFixed(2)}`;
  };
  
  // Get status badge class
  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'active': return 'status-active';
      case 'out_of_stock': return 'status-out-of-stock';
      case 'low_stock': return 'status-low-stock';
      case 'discontinued': return 'status-discontinued';
      default: return '';
    }
  };
  
  // Get status display text
  const getStatusDisplayText = (status) => {
    switch (status) {
      case 'active': return 'Active';
      case 'out_of_stock': return 'Out of Stock';
      case 'low_stock': return 'Low Stock';
      case 'discontinued': return 'Discontinued';
      default: return status;
    }
  };
  
  return (
    <div className="product-manager">
      <div className="product-manager-header">
        <h2>Product Management</h2>
        <button className="add-product-button" onClick={handleAddProduct}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Add Product
        </button>
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
      
      {/* Product Form */}
      {showForm && (
        <div className="product-form-container">
          <div className="product-form-header">
            <h3>{editMode ? 'Edit Product' : 'Add New Product'}</h3>
            <button 
              className="close-form-button" 
              onClick={() => setShowForm(false)}
              aria-label="Close form"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
          
          <form onSubmit={handleSubmit} className="product-form">
            <div className="form-section">
              <h4>Basic Information</h4>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="name">Product Name <span className="required">*</span></label>
                  <input 
                    type="text" 
                    id="name" 
                    name="name" 
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="sku">SKU <span className="required">*</span></label>
                  <input 
                    type="text" 
                    id="sku" 
                    name="sku" 
                    value={formData.sku}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="category">Category <span className="required">*</span></label>
                  <select 
                    id="category" 
                    name="category" 
                    value={formData.category}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select Category</option>
                    {categories.map(category => (
                      <option key={category} value={category}>{category}</option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="status">Status</label>
                  <select 
                    id="status" 
                    name="status" 
                    value={formData.status}
                    onChange={handleInputChange}
                  >
                    <option value="active">Active</option>
                    <option value="out_of_stock">Out of Stock</option>
                    <option value="low_stock">Low Stock</option>
                    <option value="discontinued">Discontinued</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div className="form-section">
              <h4>Pricing & Inventory</h4>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="price">Price <span className="required">*</span></label>
                  <div className="input-with-icon">
                    <span className="input-icon">$</span>
                    <input 
                      type="number" 
                      id="price" 
                      name="price" 
                      value={formData.price}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                      required
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label htmlFor="salePrice">Sale Price</label>
                  <div className="input-with-icon">
                    <span className="input-icon">$</span>
                    <input 
                      type="number" 
                      id="salePrice" 
                      name="salePrice" 
                      value={formData.salePrice}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                    />
                  </div>
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="cost">Cost</label>
                  <div className="input-with-icon">
                    <span className="input-icon">$</span>
                    <input 
                      type="number" 
                      id="cost" 
                      name="cost" 
                      value={formData.cost}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label htmlFor="quantity">Quantity</label>
                  <input 
                    type="number" 
                    id="quantity" 
                    name="quantity" 
                    value={formData.quantity}
                    onChange={handleInputChange}
                    min="0"
                  />
                </div>
              </div>
            </div>
            
            <div className="form-section">
              <h4>Description & Features</h4>
              
              <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea 
                  id="description" 
                  name="description" 
                  value={formData.description}
                  onChange={handleInputChange}
                  rows="4"
                ></textarea>
              </div>
              
              <div className="form-group">
                <label htmlFor="features">Features</label>
                <textarea 
                  id="features" 
                  name="features" 
                  value={formData.features}
                  onChange={handleInputChange}
                  rows="3"
                  placeholder="Enter features separated by commas"
                ></textarea>
              </div>
            </div>
            
            <div className="form-section">
              <h4>Images</h4>
              
              <div className="image-upload-container">
                <label htmlFor="image-upload" className="image-upload-label">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                  </svg>
                  <span>Click to upload images</span>
                </label>
                <input 
                  type="file" 
                  id="image-upload" 
                  className="image-upload" 
                  accept="image/*"
                  multiple
                  onChange={handleImageUpload}
                />
              </div>
              
              {formData.images.length > 0 && (
                <div className="image-preview-container">
                  {formData.images.map((image, index) => (
                    <div key={index} className="image-preview">
                      <img src={image.preview} alt={`Product ${index + 1}`} />
                      <button 
                        type="button" 
                        className="remove-image-button"
                        onClick={() => handleRemoveImage(index)}
                        aria-label="Remove image"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                        </svg>
                      </button>
                      <span className="image-name">{image.name}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            <div className="form-actions">
              <button 
                type="button" 
                className="cancel-button"
                onClick={() => setShowForm(false)}
                disabled={formSubmitting}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="save-button"
                disabled={formSubmitting}
              >
                {formSubmitting ? (
                  <>
                    <span className="spinner"></span>
                    <span>{editMode ? 'Updating...' : 'Saving...'}</span>
                  </>
                ) : (editMode ? 'Update Product' : 'Add Product')}
              </button>
            </div>
          </form>
        </div>
      )}
      
      {/* Filters and Search */}
      <div className="filters-container">
        <div className="search-container">
          <input 
            type="text" 
            placeholder="Search products..."
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
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Statuses</option>
            <option value="active">Active</option>
            <option value="out_of_stock">Out of Stock</option>
            <option value="low_stock">Low Stock</option>
            <option value="discontinued">Discontinued</option>
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
            <option value="price">Price</option>
            <option value="quantity">Quantity</option>
            <option value="category">Category</option>
            <option value="updatedAt">Last Updated</option>
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
      
      {/* Products Table */}
      <div className="products-table-container">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading products...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p>{error}</p>
            <button onClick={fetchProducts} className="retry-button">
              Retry
            </button>
          </div>
        ) : filteredProducts.length === 0 ? (
          <div className="empty-container">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clipRule="evenodd" />
            </svg>
            <p>No products found. Try adjusting your filters or add a new product.</p>
            <button onClick={handleAddProduct} className="add-product-button">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Product
            </button>
          </div>
        ) : (
          <>
            <table className="products-table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>SKU</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentProducts.map(product => (
                  <tr key={product.id}>
                    <td className="product-cell">
                      <div className="product-info">
                        <div className="product-image">
                          {product.images && product.images.length > 0 ? (
                            <img src={product.images[0]} alt={product.name} />
                          ) : (
                            <div className="no-image">No Image</div>
                          )}
                        </div>
                        <div>
                          <h4>{product.name}</h4>
                          <p className="product-description">{product.description}</p>
                        </div>
                      </div>
                    </td>
                    <td>{product.sku}</td>
                    <td>{product.category}</td>
                    <td>
                      {product.salePrice ? (
                        <div className="price-container">
                          <span className="sale-price">{formatCurrency(product.salePrice)}</span>
                          <span className="original-price">{formatCurrency(product.price)}</span>
                        </div>
                      ) : (
                        formatCurrency(product.price)
                      )}
                    </td>
                    <td>{product.quantity}</td>
                    <td>
                      <span className={`status-badge ${getStatusBadgeClass(product.status)}`}>
                        {getStatusDisplayText(product.status)}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="edit-button" 
                          onClick={() => handleEditProduct(product)}
                          aria-label="Edit product"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                          </svg>
                        </button>
                        <button 
                          className="delete-button" 
                          onClick={() => handleDeleteProduct(product.id)}
                          aria-label="Delete product"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                        <div className="status-dropdown">
                          <button className="status-dropdown-button">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                          </button>
                          <div className="status-dropdown-content">
                            <button 
                              onClick={() => handleStatusChange(product.id, 'active')}
                              className={product.status === 'active' ? 'active' : ''}
                            >
                              Active
                            </button>
                            <button 
                              onClick={() => handleStatusChange(product.id, 'out_of_stock')}
                              className={product.status === 'out_of_stock' ? 'active' : ''}
                            >
                              Out of Stock
                            </button>
                            <button 
                              onClick={() => handleStatusChange(product.id, 'low_stock')}
                              className={product.status === 'low_stock' ? 'active' : ''}
                            >
                              Low Stock
                            </button>
                            <button 
                              onClick={() => handleStatusChange(product.id, 'discontinued')}
                              className={product.status === 'discontinued' ? 'active' : ''}
                            >
                              Discontinued
                            </button>
                          </div>
                        </div>
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
    </div>
  );
};

export default ProductManager;