import React, { useState } from 'react';
import './ContactSupport.css';

/**
 * ContactSupport component - A responsive contact form for seller support
 * Allows sellers to submit support requests with different priority levels
 */
const ContactSupport = () => {
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    category: 'general',
    priority: 'medium',
    message: '',
    attachments: []
  });
  
  const [formStatus, setFormStatus] = useState({
    submitted: false,
    submitting: false,
    error: null
  });
  
  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };
  
  // Handle file uploads
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setFormData(prevData => ({
      ...prevData,
      attachments: [...prevData.attachments, ...files]
    }));
  };
  
  // Remove an attachment
  const removeAttachment = (index) => {
    setFormData(prevData => ({
      ...prevData,
      attachments: prevData.attachments.filter((_, i) => i !== index)
    }));
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormStatus({ submitted: false, submitting: true, error: null });
    
    try {
      // In a real app, you would send the form data to an API
      // const response = await fetch('/api/support/contact', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json'
      //   },
      //   body: JSON.stringify(formData)
      // });
      // 
      // if (!response.ok) {
      //   throw new Error('Failed to submit support request');
      // }
      
      // Simulate API call with setTimeout
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Reset form after successful submission
      setFormData({
        name: '',
        email: '',
        subject: '',
        category: 'general',
        priority: 'medium',
        message: '',
        attachments: []
      });
      
      setFormStatus({
        submitted: true,
        submitting: false,
        error: null
      });
      
      // Reset success message after 5 seconds
      setTimeout(() => {
        setFormStatus(prevStatus => ({
          ...prevStatus,
          submitted: false
        }));
      }, 5000);
      
    } catch (error) {
      setFormStatus({
        submitted: false,
        submitting: false,
        error: error.message || 'Something went wrong. Please try again.'
      });
    }
  };
  
  return (
    <div className="contact-support">
      <div className="contact-header">
        <h2>Contact Support</h2>
        <p>Our support team is here to help you with any questions or issues you may have.</p>
      </div>
      
      {formStatus.submitted && (
        <div className="success-message">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <p>Your support request has been submitted successfully. We'll get back to you soon!</p>
        </div>
      )}
      
      {formStatus.error && (
        <div className="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p>{formStatus.error}</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="contact-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="name">Your Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your name"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              required
            />
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="subject">Subject</label>
          <input
            type="text"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            placeholder="Enter subject"
            required
          />
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="general">General Inquiry</option>
              <option value="technical">Technical Support</option>
              <option value="billing">Billing & Payments</option>
              <option value="account">Account Management</option>
              <option value="orders">Orders & Shipping</option>
              <option value="products">Product Management</option>
              <option value="feature">Feature Request</option>
              <option value="bug">Bug Report</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="priority">Priority</label>
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              required
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="message">Message</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="Describe your issue or question in detail"
            rows="6"
            required
          ></textarea>
        </div>
        
        <div className="form-group">
          <label htmlFor="attachments">Attachments (Optional)</label>
          <div className="file-upload">
            <input
              type="file"
              id="attachments"
              name="attachments"
              onChange={handleFileChange}
              multiple
              className="file-input"
            />
            <label htmlFor="attachments" className="file-label">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
              <span>Choose files</span>
            </label>
          </div>
          
          {formData.attachments.length > 0 && (
            <ul className="attachment-list">
              {formData.attachments.map((file, index) => (
                <li key={index} className="attachment-item">
                  <span className="file-name">{file.name}</span>
                  <button
                    type="button"
                    className="remove-file"
                    onClick={() => removeAttachment(index)}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
        
        <div className="form-actions">
          <button
            type="submit"
            className="submit-button"
            disabled={formStatus.submitting}
          >
            {formStatus.submitting ? (
              <>
                <span className="spinner"></span>
                Submitting...
              </>
            ) : (
              'Submit Request'
            )}
          </button>
        </div>
      </form>
      
      <div className="contact-info">
        <div className="info-card">
          <div className="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div className="info-content">
            <h3>Email Support</h3>
            <p>support@onetappe.com</p>
            <p className="info-note">We typically respond within 24 hours</p>
          </div>
        </div>
        
        <div className="info-card">
          <div className="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          </div>
          <div className="info-content">
            <h3>Phone Support</h3>
            <p>+1 (555) 123-4567</p>
            <p className="info-note">Available Mon-Fri, 9am-5pm</p>
          </div>
        </div>
        
        <div className="info-card">
          <div className="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div className="info-content">
            <h3>Live Chat</h3>
            <p>Chat with our support team</p>
            <p className="info-note">Available 24/7 for urgent issues</p>
          </div>
        </div>
      </div>
      
      <div className="faq-section">
        <h3>Frequently Asked Questions</h3>
        <div className="faq-list">
          <div className="faq-item">
            <h4>How do I reset my password?</h4>
            <p>You can reset your password by clicking on the "Forgot Password" link on the login page. Follow the instructions sent to your email to create a new password.</p>
          </div>
          
          <div className="faq-item">
            <h4>How do I update my product inventory?</h4>
            <p>Navigate to the Inventory section in your dashboard. From there, you can update stock levels, add new products, or modify existing product details.</p>
          </div>
          
          <div className="faq-item">
            <h4>How do I process a refund?</h4>
            <p>Go to the Orders section, find the specific order, and click on the "Process Refund" button. Follow the prompts to complete the refund process.</p>
          </div>
          
          <div className="faq-item">
            <h4>When will I receive my payments?</h4>
            <p>Payments are typically processed within 2-3 business days after an order is marked as completed. You can view your payment schedule in the Finance section.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactSupport;