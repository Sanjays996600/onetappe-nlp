import React, { useState, useEffect } from 'react';
import './ProductLanding.css';

/**
 * ProductLanding component - A responsive landing page for product showcase
 * Features filtering, sorting, and detailed product information
 */
const ProductLanding = () => {
  // State for products data
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // State for UI controls
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [priceRange, setPriceRange] = useState({ min: 0, max: 1000 });
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [selectedProduct, setSelectedProduct] = useState(null);
  
  // Categories for filtering
  const categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty', 'Books', 'Toys'];
  
  // Fetch products data (simulated)
  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        // Simulated API call - replace with actual API integration
        setTimeout(() => {
          const sampleProducts = [
            {
              id: 1,
              name: 'Wireless Headphones',
              description: 'Premium noise-cancelling wireless headphones with 30-hour battery life.',
              price: 199.99,
              category: 'Electronics',
              rating: 4.5,
              stock: 45,
              image: 'https://via.placeholder.com/150',
              featured: true,
              tags: ['audio', 'wireless', 'premium']
            },
            {
              id: 2,
              name: 'Cotton T-Shirt',
              description: 'Comfortable 100% cotton t-shirt available in multiple colors.',
              price: 24.99,
              category: 'Clothing',
              rating: 4.2,
              stock: 120,
              image: 'https://via.placeholder.com/150',
              featured: false,
              tags: ['apparel', 'casual', 'summer']
            },
            {
              id: 3,
              name: 'Smart Coffee Maker',
              description: 'Wi-Fi enabled coffee maker that you can control with your smartphone.',
              price: 149.99,
              category: 'Home & Kitchen',
              rating: 4.0,
              stock: 30,
              image: 'https://via.placeholder.com/150',
              featured: true,
              tags: ['appliance', 'smart home', 'kitchen']
            },
            {
              id: 4,
              name: 'Vitamin C Serum',
              description: 'Anti-aging facial serum with vitamin C and hyaluronic acid.',
              price: 35.99,
              category: 'Beauty',
              rating: 4.7,
              stock: 85,
              image: 'https://via.placeholder.com/150',
              featured: false,
              tags: ['skincare', 'anti-aging', 'facial']
            },
            {
              id: 5,
              name: 'Bestselling Novel',
              description: 'The latest bestselling fiction novel everyone is talking about.',
              price: 18.99,
              category: 'Books',
              rating: 4.8,
              stock: 200,
              image: 'https://via.placeholder.com/150',
              featured: true,
              tags: ['fiction', 'bestseller', 'paperback']
            },
            {
              id: 6,
              name: 'Building Block Set',
              description: 'Educational building blocks for children ages 3-10.',
              price: 49.99,
              category: 'Toys',
              rating: 4.6,
              stock: 60,
              image: 'https://via.placeholder.com/150',
              featured: false,
              tags: ['educational', 'children', 'creative']
            },
          ];
          setProducts(sampleProducts);
          setFilteredProducts(sampleProducts);
          setLoading(false);
        }, 1000);
      } catch (err) {
        setError('Failed to load products. Please try again later.');
        setLoading(false);
      }
    };
    
    fetchProducts();
  }, []);
  
  // Filter and sort products when any filter/sort criteria changes
  useEffect(() => {
    if (!products.length) return;
    
    let result = [...products];
    
    // Apply category filter
    if (categoryFilter !== 'all') {
      result = result.filter(product => product.category === categoryFilter);
    }
    
    // Apply price range filter
    result = result.filter(
      product => product.price >= priceRange.min && product.price <= priceRange.max
    );
    
    // Apply search term filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      result = result.filter(
        product => 
          product.name.toLowerCase().includes(searchLower) ||
          product.description.toLowerCase().includes(searchLower) ||
          product.tags.some(tag => tag.toLowerCase().includes(searchLower))
      );
    }
    
    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0;
      
      switch (sortBy) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'price':
          comparison = a.price - b.price;
          break;
        case 'rating':
          comparison = b.rating - a.rating;
          break;
        default:
          comparison = 0;
      }
      
      return sortOrder === 'asc' ? comparison : -comparison;
    });
    
    setFilteredProducts(result);
  }, [products, categoryFilter, priceRange, searchTerm, sortBy, sortOrder]);
  
  // Handle product selection for detailed view
  const handleProductSelect = (product) => {
    setSelectedProduct(product);
  };
  
  // Close detailed product view
  const closeProductDetail = () => {
    setSelectedProduct(null);
  };
  
  // Handle price range change
  const handlePriceRangeChange = (e, type) => {
    const value = parseFloat(e.target.value);
    setPriceRange(prev => ({
      ...prev,
      [type]: value
    }));
  };
  
  // Render loading state
  if (loading) {
    return (
      <div className="product-landing-loading">
        <div className="spinner"></div>
        <p>Loading products...</p>
      </div>
    );
  }
  
  // Render error state
  if (error) {
    return (
      <div className="product-landing-error">
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Try Again</button>
      </div>
    );
  }
  
  return (
    <div className="product-landing-container">
      {/* Header section */}
      <div className="product-landing-header">
        <h1>Product Showcase</h1>
        <p>Discover our premium selection of high-quality products</p>
      </div>
      
      {/* Filters and controls */}
      <div className="product-landing-controls">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="filter-section">
          <div className="filter-group">
            <label>Category:</label>
            <select 
              value={categoryFilter} 
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="all">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
          
          <div className="filter-group">
            <label>Sort By:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="name">Name</option>
              <option value="price">Price</option>
              <option value="rating">Rating</option>
            </select>
            <button 
              className={`sort-order ${sortOrder === 'asc' ? 'asc' : 'desc'}`}
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              aria-label={`Sort ${sortOrder === 'asc' ? 'ascending' : 'descending'}`}
            >
              {sortOrder === 'asc' ? '↑' : '↓'}
            </button>
          </div>
          
          <div className="filter-group price-range">
            <label>Price Range:</label>
            <div className="range-inputs">
              <input 
                type="number" 
                min="0" 
                max={priceRange.max} 
                value={priceRange.min}
                onChange={(e) => handlePriceRangeChange(e, 'min')}
              />
              <span>to</span>
              <input 
                type="number" 
                min={priceRange.min} 
                value={priceRange.max}
                onChange={(e) => handlePriceRangeChange(e, 'max')}
              />
            </div>
          </div>
        </div>
        
        <div className="view-toggle">
          <button 
            className={viewMode === 'grid' ? 'active' : ''}
            onClick={() => setViewMode('grid')}
            aria-label="Grid view"
          >
            Grid
          </button>
          <button 
            className={viewMode === 'list' ? 'active' : ''}
            onClick={() => setViewMode('list')}
            aria-label="List view"
          >
            List
          </button>
        </div>
      </div>
      
      {/* Results count */}
      <div className="results-count">
        <p>{filteredProducts.length} products found</p>
      </div>
      
      {/* Product grid/list */}
      {filteredProducts.length === 0 ? (
        <div className="no-products-found">
          <p>No products match your current filters.</p>
          <button onClick={() => {
            setSearchTerm('');
            setCategoryFilter('all');
            setPriceRange({ min: 0, max: 1000 });
          }}>Clear Filters</button>
        </div>
      ) : (
        <div className={`product-${viewMode}`}>
          {filteredProducts.map(product => (
            <div 
              key={product.id} 
              className={`product-item ${product.featured ? 'featured' : ''}`}
              onClick={() => handleProductSelect(product)}
            >
              <div className="product-image">
                <img src={product.image} alt={product.name} />
                {product.featured && <span className="featured-badge">Featured</span>}
              </div>
              <div className="product-info">
                <h3>{product.name}</h3>
                {viewMode === 'list' && <p>{product.description}</p>}
                <div className="product-meta">
                  <span className="product-price">${product.price.toFixed(2)}</span>
                  <div className="product-rating">
                    <span className="stars">
                      {[...Array(5)].map((_, i) => (
                        <span 
                          key={i} 
                          className={i < Math.floor(product.rating) ? 'filled' : i < product.rating ? 'half-filled' : ''}
                        >
                          ★
                        </span>
                      ))}
                    </span>
                    <span className="rating-value">{product.rating.toFixed(1)}</span>
                  </div>
                </div>
                <div className="product-footer">
                  <span className={`stock-status ${product.stock > 10 ? 'in-stock' : product.stock > 0 ? 'low-stock' : 'out-of-stock'}`}>
                    {product.stock > 10 ? 'In Stock' : product.stock > 0 ? `Low Stock (${product.stock})` : 'Out of Stock'}
                  </span>
                  <button className="view-details-btn">View Details</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Product detail modal */}
      {selectedProduct && (
        <div className="product-detail-modal">
          <div className="modal-content">
            <button className="close-modal" onClick={closeProductDetail}>×</button>
            <div className="modal-body">
              <div className="product-detail-image">
                <img src={selectedProduct.image} alt={selectedProduct.name} />
              </div>
              <div className="product-detail-info">
                <h2>{selectedProduct.name}</h2>
                <div className="product-detail-meta">
                  <span className="product-detail-price">${selectedProduct.price.toFixed(2)}</span>
                  <div className="product-detail-rating">
                    <span className="stars">
                      {[...Array(5)].map((_, i) => (
                        <span 
                          key={i} 
                          className={i < Math.floor(selectedProduct.rating) ? 'filled' : i < selectedProduct.rating ? 'half-filled' : ''}
                        >
                          ★
                        </span>
                      ))}
                    </span>
                    <span className="rating-value">{selectedProduct.rating.toFixed(1)}</span>
                  </div>
                </div>
                <p className="product-detail-description">{selectedProduct.description}</p>
                <div className="product-detail-attributes">
                  <div className="attribute">
                    <span className="attribute-label">Category:</span>
                    <span className="attribute-value">{selectedProduct.category}</span>
                  </div>
                  <div className="attribute">
                    <span className="attribute-label">Availability:</span>
                    <span className={`attribute-value stock-status ${selectedProduct.stock > 10 ? 'in-stock' : selectedProduct.stock > 0 ? 'low-stock' : 'out-of-stock'}`}>
                      {selectedProduct.stock > 10 ? 'In Stock' : selectedProduct.stock > 0 ? `Low Stock (${selectedProduct.stock})` : 'Out of Stock'}
                    </span>
                  </div>
                  <div className="attribute">
                    <span className="attribute-label">Tags:</span>
                    <div className="attribute-value tags">
                      {selectedProduct.tags.map(tag => (
                        <span key={tag} className="tag">{tag}</span>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="product-detail-actions">
                  <button className="add-to-cart-btn" disabled={selectedProduct.stock <= 0}>
                    {selectedProduct.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
                  </button>
                  <button className="wishlist-btn">Add to Wishlist</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Pagination (simplified) */}
      <div className="pagination">
        <button disabled>Previous</button>
        <span className="page-indicator">Page 1 of 1</span>
        <button disabled>Next</button>
      </div>
    </div>
  );
};

export default ProductLanding;