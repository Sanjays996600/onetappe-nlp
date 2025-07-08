import React, { useState } from 'react';
import './FAQSection.css';

/**
 * FAQSection component - A responsive FAQ section with expandable questions and answers
 * Features:
 * - Accordion-style expandable questions
 * - Category filtering
 * - Search functionality
 * - Responsive design for all screen sizes
 */
const FAQSection = () => {
  // Sample FAQ data
  const faqData = [
    {
      id: 1,
      question: 'How do I add a new product to my inventory?',
      answer: 'To add a new product, navigate to the Products section in your dashboard and click on "Add New Product". Fill in the required details such as product name, description, price, and inventory quantity. You can also add product images and set categories. Once complete, click "Save" to add the product to your inventory.',
      category: 'Products'
    },
    {
      id: 2,
      question: 'How can I generate an invoice for an order?',
      answer: 'To generate an invoice, go to the Orders section and find the specific order. Click on the "Generate Invoice" button next to the order. You can customize the invoice by adding discounts or special notes before generating. Once ready, click "Generate" and you can download the invoice as a PDF or send it directly to the customer via email.',
      category: 'Orders'
    },
    {
      id: 3,
      question: 'How do I view my sales analytics?',
      answer: 'To view your sales analytics, navigate to the Sales Analytics section in your dashboard. Here you can see various charts and metrics showing your sales performance over time. You can filter the data by date range, product category, or sales channel. The dashboard provides insights on total sales, average order value, top-selling products, and more.',
      category: 'Analytics'
    },
    {
      id: 4,
      question: 'How can I update my store settings?',
      answer: 'To update your store settings, go to the Settings section in your dashboard. Here you can modify your store name, logo, contact information, shipping options, payment methods, and notification preferences. Make sure to click "Save Changes" after making any modifications to ensure they are applied to your store.',
      category: 'Settings'
    },
    {
      id: 5,
      question: 'How do I process a customer refund?',
      answer: 'To process a refund, go to the Orders section and locate the specific order. Click on "View Details" and then select the "Process Refund" option. You can choose to refund the full amount or a partial amount. Add a reason for the refund and any additional notes. Once submitted, the refund will be processed through the original payment method used by the customer.',
      category: 'Orders'
    },
    {
      id: 6,
      question: 'How can I customize my product catalog landing page?',
      answer: 'To customize your product catalog landing page, go to the Product Catalog section and click on "Customize Layout". Here you can arrange the display order of products, choose between grid or list view, set featured products, and customize filters. You can also add a banner image and promotional text to enhance the visual appeal of your catalog page.',
      category: 'Products'
    },
    {
      id: 7,
      question: 'How do I set up automated inventory alerts?',
      answer: 'To set up inventory alerts, navigate to the Inventory section and click on "Alert Settings". Here you can define threshold levels for low stock warnings. When a product quantity falls below the specified threshold, you will receive notifications via email or dashboard alerts. You can also enable automatic reorder notifications to streamline your inventory management process.',
      category: 'Inventory'
    },
    {
      id: 8,
      question: 'How can I contact customer support?',
      answer: 'To contact our support team, click on the "Contact Support" link in the sidebar. Fill out the contact form with your issue details, and our team will respond within 24 hours. For urgent matters, you can use the live chat feature available during business hours or call our dedicated support line at the number provided in the Contact Support page.',
      category: 'Support'
    },
    {
      id: 9,
      question: 'How do I create and manage discount codes?',
      answer: 'To create discount codes, go to the Marketing section and select "Discount Codes". Click on "Create New Code" and specify the discount type (percentage or fixed amount), value, applicable products, usage limits, and expiration date. You can view analytics on code usage and manage existing codes from the same section.',
      category: 'Marketing'
    },
    {
      id: 10,
      question: 'How can I export my sales and inventory reports?',
      answer: 'To export reports, navigate to the Reports section in your dashboard. Select the type of report you want to export (sales, inventory, customer, etc.) and set the date range. Choose your preferred format (CSV, Excel, or PDF) and click "Generate Report". Once generated, you can download the report or set up automated scheduled exports to be sent to your email.',
      category: 'Reports'
    }
  ];

  // State management
  const [activeId, setActiveId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  // Get unique categories
  const categories = ['All', ...new Set(faqData.map(item => item.category))];

  // Filter FAQs based on search query and selected category
  const filteredFAQs = faqData.filter(faq => {
    const matchesSearch = faq.question.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         faq.answer.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || faq.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Toggle FAQ item
  const toggleFAQ = (id) => {
    setActiveId(activeId === id ? null : id);
  };

  return (
    <div className="faq-container">
      <div className="faq-header">
        <h2>Frequently Asked Questions</h2>
        <p>Find answers to common questions about using our seller dashboard</p>
      </div>

      {/* Search and filter */}
      <div className="faq-controls">
        <div className="faq-search">
          <input
            type="text"
            placeholder="Search questions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>

        <div className="faq-categories">
          {categories.map(category => (
            <button
              key={category}
              className={selectedCategory === category ? 'active' : ''}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* FAQ list */}
      <div className="faq-list">
        {filteredFAQs.length > 0 ? (
          filteredFAQs.map(faq => (
            <div key={faq.id} className={`faq-item ${activeId === faq.id ? 'active' : ''}`}>
              <div className="faq-question" onClick={() => toggleFAQ(faq.id)}>
                <h3>{faq.question}</h3>
                <div className="faq-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    {activeId === faq.id ? (
                      <line x1="18" y1="12" x2="6" y2="12"></line>
                    ) : (
                      <>
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                      </>
                    )}
                  </svg>
                </div>
              </div>
              <div className="faq-answer">
                <p>{faq.answer}</p>
                <span className="faq-category">{faq.category}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="faq-empty">
            <p>No questions found matching your search.</p>
            <button onClick={() => {
              setSearchQuery('');
              setSelectedCategory('All');
            }}>
              Clear filters
            </button>
          </div>
        )}
      </div>

      {/* Still have questions section */}
      <div className="faq-contact">
        <h3>Still have questions?</h3>
        <p>If you cannot find an answer to your question, our support team is here to help.</p>
        <div className="faq-contact-buttons">
          <a href="/seller-dashboard/contact" className="contact-button primary">
            Contact Support
          </a>
          <a href="#" className="contact-button secondary">
            View Documentation
          </a>
        </div>
      </div>
    </div>
  );
};

export default FAQSection;