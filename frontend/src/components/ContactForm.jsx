import React, { useState } from 'react';
import './ContactForm.css';

/**
 * ContactForm component - A responsive contact form for customer inquiries
 * Features form validation, responsive design, and submission handling
 */
const ContactForm = () => {
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  
  // Form status state
  const [status, setStatus] = useState({
    submitted: false,
    submitting: false,
    info: { error: false, msg: null }
  });
  
  // Form validation state
  const [errors, setErrors] = useState({});
  
  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({ ...prevState, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prevErrors => ({ ...prevErrors, [name]: null }));
    }
  };
  
  // Validate form
  const validateForm = () => {
    const newErrors = {};
    
    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    // Subject validation
    if (!formData.subject.trim()) {
      newErrors.subject = 'Subject is required';
    }
    
    // Message validation
    if (!formData.message.trim()) {
      newErrors.message = 'Message is required';
    } else if (formData.message.trim().length < 10) {
      newErrors.message = 'Message must be at least 10 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setStatus(prevStatus => ({ ...prevStatus, submitting: true }));
    
    // Simulate API call with setTimeout
    setTimeout(() => {
      // In a real application, you would submit to an API endpoint:
      // try {
      //   const response = await fetch('/api/contact', {
      //     method: 'POST',
      //     headers: { 'Content-Type': 'application/json' },
      //     body: JSON.stringify(formData)
      //   });
      //   
      //   if (!response.ok) throw new Error('Failed to submit form');
      //   
      //   setFormData({ name: '', email: '', subject: '', message: '' });
      //   setStatus({
      //     submitted: true,
      //     submitting: false,
      //     info: { error: false, msg: 'Thank you for your message! We will get back to you soon.' }
      //   });
      // } catch (error) {
      //   setStatus({
      //     submitted: false,
      //     submitting: false,
      //     info: { error: true, msg: 'Something went wrong. Please try again later.' }
      //   });
      // }
      
      // For demo purposes, we'll simulate a successful submission
      setFormData({ name: '', email: '', subject: '', message: '' });
      setStatus({
        submitted: true,
        submitting: false,
        info: { error: false, msg: 'Thank you for your message! We will get back to you soon.' }
      });
    }, 1500);
  };
  
  return (
    <div className="contact-form-container">
      <div className="contact-form-card">
        <div className="contact-form-header">
          <h2>Contact Us</h2>
          <p>Have questions or need assistance? Send us a message and we'll respond as soon as possible.</p>
        </div>
        
        {status.info.msg && (
          <div className={`contact-form-alert ${status.info.error ? 'error' : 'success'}`}>
            {status.info.msg}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="contact-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Your name"
              className={errors.name ? 'error' : ''}
              disabled={status.submitting}
            />
            {errors.name && <span className="error-message">{errors.name}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Your email address"
              className={errors.email ? 'error' : ''}
              disabled={status.submitting}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="subject">Subject</label>
            <input
              type="text"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              placeholder="Subject of your message"
              className={errors.subject ? 'error' : ''}
              disabled={status.submitting}
            />
            {errors.subject && <span className="error-message">{errors.subject}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="message">Message</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Your message"
              rows="5"
              className={errors.message ? 'error' : ''}
              disabled={status.submitting}
            ></textarea>
            {errors.message && <span className="error-message">{errors.message}</span>}
          </div>
          
          <button 
            type="submit" 
            className="submit-button" 
            disabled={status.submitting || status.submitted}
          >
            {status.submitting ? (
              <>
                <span className="spinner"></span>
                <span>Sending...</span>
              </>
            ) : status.submitted ? (
              'Message Sent'
            ) : (
              'Send Message'
            )}
          </button>
        </form>
        
        <div className="contact-info">
          <div className="contact-method">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="contact-icon">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <div>
              <h3>Email Us</h3>
              <p>support@onetappe.com</p>
            </div>
          </div>
          
          <div className="contact-method">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="contact-icon">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <div>
              <h3>Call Us</h3>
              <p>+1 (555) 123-4567</p>
            </div>
          </div>
          
          <div className="contact-method">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="contact-icon">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <div>
              <h3>Visit Us</h3>
              <p>123 Business Street, Suite 100<br />San Francisco, CA 94103</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactForm;