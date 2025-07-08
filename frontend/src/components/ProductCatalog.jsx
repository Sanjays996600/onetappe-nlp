import React, { useState, useEffect, useCallback } from 'react';
import './ProductCatalog.css';

/**
 * ProductCatalog component for displaying a responsive product catalog
 * This component provides a dynamic landing page for product listings
 * with filtering, sorting, and responsive grid/list views
 * 
 * Enhanced with improved mobile responsiveness and API integration
 */
const ProductCatalog = ({ initialProducts = [], categories = [], apiEndpoint = '/api/products' }) => {
  const [products, setProducts] = useState(initialProducts);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [sortBy, setSortBy] = useState('name-asc');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isFilterMenuOpen, setIsFilterMenuOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [productsPerPage] = useState(12);
  const [totalProducts, setTotalProducts] = useState(0);
  
  // Fetch products function with API integration and error handling
  const fetchProducts = useCallback(async (page = 1, category = 'all', search = '', sort = 'name-asc') => {
    if (initialProducts.length > 0 && page === 1) {
      setProducts(initialProducts);
      setTotalProducts(initialProducts.length);
      setLoading(false);
      return;
    }
    
    setLoading(true);
    
    try {
      // In a production environment, use the actual API endpoint
      // with proper query parameters for filtering, sorting, and pagination
      const queryParams = new URLSearchParams({
        page,
        limit: productsPerPage,
        category: category !== 'all' ? category : '',
        search,
        sort
      }).toString();
      
      // For demo purposes, we'll simulate an API call
      // In production, uncomment this code and remove the setTimeout
      // const response = await fetch(`${apiEndpoint}?${queryParams}`);
      // if (!response.ok) throw new Error('Network response was not ok');
      // const data = await response.json();
      // setProducts(data.products);
      // setTotalProducts(data.total);
      
      // Simulate API call with setTimeout
      setTimeout(() => {
        try {
          // Sample data - in a real app, this would come from an API
          const sampleProducts = [
            {
              id: 1,
              name: 'Premium T-Shirt',
              category: 'clothing',
              price: 19.99,
              image: 'https://via.placeholder.com/300x300?text=T-Shirt',
              description: 'High-quality cotton t-shirt with custom design.',
              inStock: true,
              rating: 4.5,
              createdAt: '2023-08-15',
            },
            {
              id: 2,
              name: 'Designer Jeans',
              category: 'clothing',
              price: 39.99,
              image: 'https://via.placeholder.com/300x300?text=Jeans',
              description: 'Stylish jeans with perfect fit and comfort.',
              inStock: true,
              rating: 4.2,
              createdAt: '2023-07-20',
            },
            {
              id: 3,
              name: 'Leather Wallet',
              category: 'accessories',
              price: 24.99,
              image: 'https://via.placeholder.com/300x300?text=Wallet',
              description: 'Genuine leather wallet with multiple card slots.',
              inStock: true,
              rating: 4.8,
              createdAt: '2023-09-05',
            },
            {
              id: 4,
              name: 'Wireless Earbuds',
              category: 'electronics',
              price: 49.99,
              image: 'https://via.placeholder.com/300x300?text=Earbuds',
              description: 'High-quality sound with noise cancellation.',
              inStock: false,
              rating: 4.7,
              createdAt: '2023-06-10',
            },
            {
              id: 5,
              name: 'Smart Watch',
              category: 'electronics',
              price: 99.99,
              image: 'https://via.placeholder.com/300x300?text=Watch',
              description: 'Track your fitness and stay connected.',
              inStock: true,
              rating: 4.4,
              createdAt: '2023-08-25',
            },
            {
              id: 6,
              name: 'Yoga Mat',
              category: 'fitness',
              price: 29.99,
              image: 'https://via.placeholder.com/300x300?text=Yoga+Mat',
              description: 'Non-slip surface for comfortable workouts.',
              inStock: true,
              rating: 4.3,
              createdAt: '2023-07-15',
            },
            {
              id: 7,
              name: 'Running Shoes',
              category: 'fitness',
              price: 89.99,
              image: 'https://via.placeholder.com/300x300?text=Running+Shoes',
              description: 'Comfortable running shoes with excellent support.',
              inStock: true,
              rating: 4.6,
              createdAt: '2023-09-10',
            },
            {
              id: 8,
              name: 'Bluetooth Speaker',
              category: 'electronics',
              price: 59.99,
              image: 'https://via.placeholder.com/300x300?text=Speaker',
              description: 'Portable speaker with rich sound quality.',
              inStock: true,
              rating: 4.5,
              createdAt: '2023-08-05',
            },
          ];
          
          // Filter based on category and search
          let filtered = sampleProducts;
          
          if (category !== 'all') {
            filtered = filtered.filter(p => p.category === category);
          }
          
          if (search) {
            const query = search.toLowerCase();
            filtered = filtered.filter(p => 
              p.name.toLowerCase().includes(query) || 
              p.description.toLowerCase().includes(query)
            );
          }
          
          // Sort products
          switch (sort) {
            case 'name-asc':
              filtered.sort((a, b) => a.name.localeCompare(b.name));
              break;
            case 'name-desc':
              filtered.sort((a, b) => b.name.localeCompare(a.name));
              break;
            case 'price-asc':
              filtered.sort((a, b) => a.price - b.price);
              break;
            case 'price-desc':
              filtered.sort((a, b) => b.price - a.price);
              break;
            case 'rating':
              filtered.sort((a, b) => b.rating - a.rating);
              break;
            default:
              break;
          }
          
          // Paginate
          const startIndex = (page - 1) * productsPerPage;
          const paginatedProducts = filtered.slice(startIndex, startIndex + productsPerPage);
          
          setProducts(paginatedProducts);
          setTotalProducts(filtered.length);
          setLoading(false);
        } catch (err) {
          console.error('Error processing products:', err);
          setError('Failed to process products');
          setLoading(false);
        }
      }, 800);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products. Please check your connection and try again.');
      setLoading(false);
    }
  }, [apiEndpoint, initialProducts, productsPerPage]);
  
  // Fetch products when component mounts or when dependencies change
  useEffect(() => {
    fetchProducts(currentPage, selectedCategory, searchQuery, sortBy);
  }, [fetchProducts, currentPage, selectedCategory, searchQuery, sortBy]);
  
  // Set filtered products based on the fetched products
  useEffect(() => {
    setFilteredProducts(products);
  }, [products]);
  
  // Handle filter and sort changes
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    
    // Reset to page 1 when changing filters
    setCurrentPage(1);
    
    switch (name) {
      case 'category':
        setSelectedCategory(value);
        break;
      case 'sort':
        setSortBy(value);
        break;
      default:
        break;
    }
  };
  
  // Handle search input changes with debounce
  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    setCurrentPage(1); // Reset to page 1 when searching
  };
  
  // Handle pagination
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    // Scroll to top when changing pages
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  // Calculate pagination information
  const totalPages = Math.ceil(totalProducts / productsPerPage);
  const pageNumbers = [];
  
  // Generate page numbers for pagination
  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }
  
  // Get unique categories from products
  const availableCategories = categories.length > 0 
    ? categories 
    : ['all', ...new Set(products.map(product => product.category))];
  
  if (error) {
    return <div className="product-catalog-error">{error}</div>;
  }
  
  return (
    <div className="product-catalog-container">
      {/* Hero Banner for Landing Page */}
      <div className="product-catalog-hero">
        <div className="hero-content">
          <h1>Discover Amazing Products</h1>
          <p>Browse our collection of high-quality items</p>
          <div className="hero-search">
            <input 
              type="text" 
              placeholder="Search products..." 
              value={searchQuery}
              onChange={handleSearchChange}
              aria-label="Search products"
            />
            <button className="search-btn" onClick={() => handleSearchChange({ target: { value: searchQuery } })}>
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <div className="product-catalog-header">
        <div className="header-top">
          <h2>{searchQuery ? `Search Results for "${searchQuery}"` : 'Product Catalog'}</h2>
          
          {/* Mobile Filter Toggle Button */}
          <button 
            className="filter-toggle-btn"
            onClick={() => setIsFilterMenuOpen(!isFilterMenuOpen)}
            aria-expanded={isFilterMenuOpen}
            aria-controls="filter-menu"
          >
            <svg viewBox="0 0 24 24" width="18" height="18">
              <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" />
            </svg>
            Filters
          </button>
        </div>
        
        <div className={`product-catalog-controls ${isFilterMenuOpen ? 'open' : ''}`} id="filter-menu">
          <div className="search-bar">
            <input 
              type="text" 
              placeholder="Search products..." 
              value={searchQuery}
              onChange={handleSearchChange}
              aria-label="Search products"
            />
          </div>
          
          <div className="filter-sort-controls">
            <div className="category-filter">
              <label htmlFor="category-select">Category:</label>
              <select 
                id="category-select" 
                name="category"
                value={selectedCategory}
                onChange={handleFilterChange}
              >
                {availableCategories.map((category, index) => (
                  <option key={index} value={category === 'all' ? 'all' : category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="sort-control">
              <label htmlFor="sort-select">Sort by:</label>
              <select 
                id="sort-select" 
                name="sort"
                value={sortBy}
                onChange={handleFilterChange}
              >
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="price-asc">Price (Low to High)</option>
                <option value="price-desc">Price (High to Low)</option>
                <option value="rating">Rating</option>
              </select>
            </div>
            
            <div className="view-toggle">
              <button 
                className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
                onClick={() => setViewMode('grid')}
                aria-label="Grid view"
              >
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zm0 11h7v7h-7v-7zm-11 0h7v7H3v-7z" />
                </svg>
              </button>
              <button 
                className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
                onClick={() => setViewMode('list')}
                aria-label="List view"
              >
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <path d="M3 4h18v2H3V4zm0 7h18v2H3v-2zm0 7h18v2H3v-2z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        {/* Results count */}
        <div className="results-count">
          Showing {filteredProducts.length} of {totalProducts} products
        </div>
      </div>
      
      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner">
            <svg viewBox="0 0 50 50" className="spinner">
              <circle cx="25" cy="25" r="20" fill="none" strokeWidth="5"></circle>
            </svg>
          </div>
          <p>Loading products...</p>
        </div>
      ) : filteredProducts.length === 0 ? (
        <div className="no-products-message">
          <p>No products found matching your criteria.</p>
          <button 
            className="reset-filters-btn"
            onClick={() => {
              setSelectedCategory('all');
              setSearchQuery('');
              setSortBy('name-asc');
              setCurrentPage(1);
            }}
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <>
          <div className={`product-${viewMode}-view`}>
            {filteredProducts.map(product => (
              <div key={product.id} className={`product-${viewMode}-item`}>
                <div className="product-image">
                  <img src={product.image} alt={product.name} loading="lazy" />
                  {!product.inStock && <span className="out-of-stock-badge">Out of Stock</span>}
                </div>
                
                <div className="product-details">
                  <h3 className="product-name">{product.name}</h3>
                  
                  <div className="product-category">{product.category}</div>
                  
                  <div className="product-rating">
                    {[...Array(5)].map((_, i) => (
                      <span key={i} className={i < Math.floor(product.rating) ? 'star filled' : 'star'}>
                        ★
                      </span>
                    ))}
                    <span className="rating-value">{product.rating.toFixed(1)}</span>
                  </div>
                  
                  <p className="product-description">{product.description}</p>
                  
                  <div className="product-price-actions">
                    <div className="product-price">${product.price.toFixed(2)}</div>
                    
                    <div className="product-actions">
                      <button 
                        className="view-details-btn"
                        onClick={() => alert(`View details for ${product.name}`)}
                      >
                        View Details
                      </button>
                      
                      <button 
                        className={`add-to-cart-btn ${!product.inStock ? 'disabled' : ''}`}
                        disabled={!product.inStock}
                        onClick={() => product.inStock && alert(`Added ${product.name} to cart`)}
                      >
                        {product.inStock ? 'Add to Cart' : 'Out of Stock'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pagination">
              <button 
                className="pagination-btn"
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
              >
                &laquo; Previous
              </button>
              
              <div className="page-numbers">
                {pageNumbers.map(number => (
                  <button
                    key={number}
                    className={`page-number ${currentPage === number ? 'active' : ''}`}
                    onClick={() => handlePageChange(number)}
                  >
                    {number}
                  </button>
                ))}
              </div>
              
              <button 
                className="pagination-btn"
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                Next &raquo;
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ProductCatalog;