import React, { useState, useEffect } from 'react';
import './TestimonialsLanding.css';

/**
 * TestimonialsLanding component - A responsive landing page for customer testimonials
 * Features:
 * - Responsive grid layout for testimonials
 * - Filtering by rating and category
 * - Animated testimonial cards
 * - Pagination for large sets of testimonials
 */
const TestimonialsLanding = () => {
  // Sample testimonial data
  const sampleTestimonials = [
    {
      id: 1,
      name: 'Sarah Johnson',
      role: 'Fashion Retailer',
      rating: 5,
      date: '2023-10-15',
      category: 'Platform',
      content: 'This dashboard has completely transformed how I manage my inventory. The analytics tools have helped me identify trends and make better purchasing decisions.',
      avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
    },
    {
      id: 2,
      name: 'Michael Chen',
      role: 'Electronics Seller',
      rating: 4,
      date: '2023-09-22',
      category: 'Support',
      content: 'The customer support team is incredibly responsive. Any issues I encounter are resolved within hours, allowing me to focus on growing my business.',
      avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
    },
    {
      id: 3,
      name: 'Emma Rodriguez',
      role: 'Handmade Crafts',
      rating: 5,
      date: '2023-11-05',
      category: 'Sales',
      content: 'Since implementing the dynamic landing pages, my conversion rate has increased by 35%. The customizable templates are perfect for showcasing my handmade products.',
      avatar: 'https://randomuser.me/api/portraits/women/63.jpg'
    },
    {
      id: 4,
      name: 'David Kim',
      role: 'Book Seller',
      rating: 5,
      date: '2023-10-30',
      category: 'Platform',
      content: 'The invoice generation feature has saved me countless hours of administrative work. The professional-looking invoices have improved my brand image with customers.',
      avatar: 'https://randomuser.me/api/portraits/men/11.jpg'
    },
    {
      id: 5,
      name: 'Olivia Martinez',
      role: 'Beauty Products',
      rating: 4,
      date: '2023-09-18',
      category: 'Sales',
      content: 'The sales analytics dashboard provides insights that have helped me optimize my product offerings. I can now easily identify which products are performing best.',
      avatar: 'https://randomuser.me/api/portraits/women/26.jpg'
    },
    {
      id: 6,
      name: 'James Wilson',
      role: 'Home Goods',
      rating: 3,
      date: '2023-11-12',
      category: 'Platform',
      content: 'The platform is generally good, though there are some features I wish were more intuitive. The mobile responsiveness could be improved for on-the-go management.',
      avatar: 'https://randomuser.me/api/portraits/men/59.jpg'
    },
    {
      id: 7,
      name: 'Sophia Lee',
      role: 'Jewelry Designer',
      rating: 5,
      date: '2023-10-08',
      category: 'Support',
      content: 'The onboarding process was seamless, and the support team guided me through every step. I was able to set up my entire store in just one afternoon.',
      avatar: 'https://randomuser.me/api/portraits/women/33.jpg'
    },
    {
      id: 8,
      name: 'Daniel Garcia',
      role: 'Sports Equipment',
      rating: 4,
      date: '2023-09-29',
      category: 'Sales',
      content: 'The product catalog feature has made it easy to organize my large inventory of sports equipment. Customers can now find exactly what they need quickly.',
      avatar: 'https://randomuser.me/api/portraits/men/18.jpg'
    },
    {
      id: 9,
      name: 'Ava Thompson',
      role: 'Organic Food',
      rating: 5,
      date: '2023-11-20',
      category: 'Platform',
      content: 'As someone selling perishable goods, the inventory management system has been a lifesaver. I can track expiration dates and reduce waste significantly.',
      avatar: 'https://randomuser.me/api/portraits/women/9.jpg'
    }
  ];

  // State management
  const [testimonials, setTestimonials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState({
    rating: 0, // 0 means all ratings
    category: 'All'
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(6);

  // Fetch testimonials (simulated)
  useEffect(() => {
    const fetchTestimonials = () => {
      setLoading(true);
      try {
        // Simulate API call delay
        setTimeout(() => {
          setTestimonials(sampleTestimonials);
          setLoading(false);
        }, 800);
      } catch (err) {
        setError('Failed to load testimonials. Please try again later.');
        setLoading(false);
      }
    };

    fetchTestimonials();
  }, []);

  // Filter testimonials based on current filter settings
  const filteredTestimonials = testimonials.filter(testimonial => {
    return (
      (filter.rating === 0 || testimonial.rating >= filter.rating) &&
      (filter.category === 'All' || testimonial.category === filter.category)
    );
  });

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentTestimonials = filteredTestimonials.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredTestimonials.length / itemsPerPage);

  // Handle filter changes
  const handleRatingFilter = (rating) => {
    setFilter({ ...filter, rating });
    setCurrentPage(1); // Reset to first page when filter changes
  };

  const handleCategoryFilter = (category) => {
    setFilter({ ...filter, category });
    setCurrentPage(1); // Reset to first page when filter changes
  };

  // Handle pagination
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  // Render star ratings
  const renderStars = (rating) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={i <= rating ? 'star filled' : 'star'}>
          ★
        </span>
      );
    }
    return stars;
  };

  // Get unique categories from testimonials
  const categories = ['All', ...new Set(testimonials.map(item => item.category))];

  return (
    <div className="testimonials-container">
      <div className="testimonials-header">
        <h2>Customer Testimonials</h2>
        <p>See what our sellers are saying about their experience with our platform</p>
      </div>

      {/* Filters */}
      <div className="testimonials-filters">
        <div className="filter-group">
          <label>Filter by Rating:</label>
          <div className="rating-filter">
            <button 
              className={filter.rating === 0 ? 'active' : ''}
              onClick={() => handleRatingFilter(0)}
            >
              All
            </button>
            {[3, 4, 5].map(rating => (
              <button 
                key={rating}
                className={filter.rating === rating ? 'active' : ''}
                onClick={() => handleRatingFilter(rating)}
              >
                {rating}+ ★
              </button>
            ))}
          </div>
        </div>

        <div className="filter-group">
          <label>Filter by Category:</label>
          <div className="category-filter">
            {categories.map(category => (
              <button 
                key={category}
                className={filter.category === category ? 'active' : ''}
                onClick={() => handleCategoryFilter(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="testimonials-loading">
          <div className="spinner"></div>
          <p>Loading testimonials...</p>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="testimonials-error">
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Try Again</button>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && filteredTestimonials.length === 0 && (
        <div className="testimonials-empty">
          <p>No testimonials match your current filters.</p>
          <button onClick={() => setFilter({ rating: 0, category: 'All' })}>Clear Filters</button>
        </div>
      )}

      {/* Testimonials grid */}
      {!loading && !error && filteredTestimonials.length > 0 && (
        <div className="testimonials-grid">
          {currentTestimonials.map(testimonial => (
            <div key={testimonial.id} className="testimonial-card">
              <div className="testimonial-header">
                <img 
                  src={testimonial.avatar} 
                  alt={`${testimonial.name}'s avatar`} 
                  className="testimonial-avatar" 
                />
                <div className="testimonial-meta">
                  <h3>{testimonial.name}</h3>
                  <p className="testimonial-role">{testimonial.role}</p>
                  <div className="testimonial-rating">
                    {renderStars(testimonial.rating)}
                  </div>
                </div>
              </div>
              <div className="testimonial-content">
                <p>"{testimonial.content}"</p>
              </div>
              <div className="testimonial-footer">
                <span className="testimonial-date">
                  {new Date(testimonial.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                  })}
                </span>
                <span className="testimonial-category">{testimonial.category}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {!loading && !error && totalPages > 1 && (
        <div className="testimonials-pagination">
          <button 
            onClick={() => paginate(currentPage - 1)} 
            disabled={currentPage === 1}
            className="pagination-button"
          >
            &laquo; Previous
          </button>
          
          <div className="pagination-numbers">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(number => (
              <button
                key={number}
                onClick={() => paginate(number)}
                className={currentPage === number ? 'active' : ''}
              >
                {number}
              </button>
            ))}
          </div>
          
          <button 
            onClick={() => paginate(currentPage + 1)} 
            disabled={currentPage === totalPages}
            className="pagination-button"
          >
            Next &raquo;
          </button>
        </div>
      )}

      {/* Call to action */}
      <div className="testimonials-cta">
        <h3>Share Your Experience</h3>
        <p>We'd love to hear about your experience with our platform.</p>
        <button className="cta-button">Submit Your Testimonial</button>
      </div>
    </div>
  );
};

export default TestimonialsLanding;