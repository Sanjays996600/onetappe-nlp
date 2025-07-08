import React, { useState } from 'react';
import './SettingsManager.css';

/**
 * SettingsManager component - A responsive settings page with user profile management,
 * notification preferences, and account settings
 */
const SettingsManager = () => {
  // Tabs state
  const [activeTab, setActiveTab] = useState('profile');
  
  // Profile settings state
  const [profileForm, setProfileForm] = useState({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    phone: '(555) 123-4567',
    company: 'Acme Inc.',
    bio: 'Experienced seller with 5+ years in e-commerce.',
    avatar: null,
    avatarPreview: 'https://randomuser.me/api/portraits/men/41.jpg'
  });
  
  // Notification settings state
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    orderUpdates: true,
    productAlerts: true,
    inventoryAlerts: true,
    marketingEmails: false,
    smsNotifications: false,
    browserNotifications: true
  });
  
  // Account settings state
  const [accountSettings, setAccountSettings] = useState({
    language: 'english',
    timezone: 'UTC-5',
    currency: 'usd',
    twoFactorAuth: false,
    autoSave: true,
    darkMode: false
  });
  
  // Password change state
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  
  // Form submission states
  const [profileSubmitting, setProfileSubmitting] = useState(false);
  const [notificationsSubmitting, setNotificationsSubmitting] = useState(false);
  const [accountSubmitting, setAccountSubmitting] = useState(false);
  const [passwordSubmitting, setPasswordSubmitting] = useState(false);
  
  // Success/error messages
  const [profileMessage, setProfileMessage] = useState({ type: null, text: null });
  const [notificationsMessage, setNotificationsMessage] = useState({ type: null, text: null });
  const [accountMessage, setAccountMessage] = useState({ type: null, text: null });
  const [passwordMessage, setPasswordMessage] = useState({ type: null, text: null });
  
  // Handle tab change
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };
  
  // Handle profile form changes
  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileForm(prev => ({ ...prev, [name]: value }));
  };
  
  // Handle avatar upload
  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProfileForm(prev => ({ ...prev, avatar: file }));
      
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileForm(prev => ({ ...prev, avatarPreview: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };
  
  // Handle notification toggle
  const handleNotificationToggle = (setting) => {
    setNotificationSettings(prev => ({
      ...prev,
      [setting]: !prev[setting]
    }));
  };
  
  // Handle account settings change
  const handleAccountSettingChange = (e) => {
    const { name, value, type, checked } = e.target;
    setAccountSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };
  
  // Handle password form changes
  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordForm(prev => ({ ...prev, [name]: value }));
  };
  
  // Handle profile form submission
  const handleProfileSubmit = (e) => {
    e.preventDefault();
    setProfileSubmitting(true);
    setProfileMessage({ type: null, text: null });
    
    // Simulate API call
    setTimeout(() => {
      setProfileSubmitting(false);
      setProfileMessage({ 
        type: 'success', 
        text: 'Profile updated successfully!' 
      });
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setProfileMessage({ type: null, text: null });
      }, 3000);
    }, 1500);
  };
  
  // Handle notifications form submission
  const handleNotificationsSubmit = (e) => {
    e.preventDefault();
    setNotificationsSubmitting(true);
    setNotificationsMessage({ type: null, text: null });
    
    // Simulate API call
    setTimeout(() => {
      setNotificationsSubmitting(false);
      setNotificationsMessage({ 
        type: 'success', 
        text: 'Notification preferences saved!' 
      });
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setNotificationsMessage({ type: null, text: null });
      }, 3000);
    }, 1500);
  };
  
  // Handle account settings form submission
  const handleAccountSubmit = (e) => {
    e.preventDefault();
    setAccountSubmitting(true);
    setAccountMessage({ type: null, text: null });
    
    // Simulate API call
    setTimeout(() => {
      setAccountSubmitting(false);
      setAccountMessage({ 
        type: 'success', 
        text: 'Account settings updated!' 
      });
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setAccountMessage({ type: null, text: null });
      }, 3000);
    }, 1500);
  };
  
  // Handle password change form submission
  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    
    // Validate passwords match
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setPasswordMessage({ 
        type: 'error', 
        text: 'New passwords do not match.' 
      });
      return;
    }
    
    setPasswordSubmitting(true);
    setPasswordMessage({ type: null, text: null });
    
    // Simulate API call
    setTimeout(() => {
      setPasswordSubmitting(false);
      setPasswordMessage({ 
        type: 'success', 
        text: 'Password changed successfully!' 
      });
      
      // Clear form
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setPasswordMessage({ type: null, text: null });
      }, 3000);
    }, 1500);
  };
  
  return (
    <div className="settings-manager">
      <div className="settings-header">
        <h2>Account Settings</h2>
        <p>Manage your profile, preferences, and account settings</p>
      </div>
      
      <div className="settings-container">
        {/* Settings Tabs */}
        <div className="settings-tabs">
          <button 
            className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => handleTabChange('profile')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
            Profile
          </button>
          
          <button 
            className={`tab-button ${activeTab === 'notifications' ? 'active' : ''}`}
            onClick={() => handleTabChange('notifications')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
            </svg>
            Notifications
          </button>
          
          <button 
            className={`tab-button ${activeTab === 'account' ? 'active' : ''}`}
            onClick={() => handleTabChange('account')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
            </svg>
            Account
          </button>
          
          <button 
            className={`tab-button ${activeTab === 'security' ? 'active' : ''}`}
            onClick={() => handleTabChange('security')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
            </svg>
            Security
          </button>
        </div>
        
        {/* Settings Content */}
        <div className="settings-content">
          {/* Profile Settings */}
          {activeTab === 'profile' && (
            <div className="settings-panel">
              <h3>Profile Information</h3>
              <p className="panel-description">Update your personal information and profile picture</p>
              
              {profileMessage.text && (
                <div className={`message ${profileMessage.type}`}>
                  {profileMessage.type === 'success' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  )}
                  <span>{profileMessage.text}</span>
                </div>
              )}
              
              <form onSubmit={handleProfileSubmit} className="settings-form">
                <div className="avatar-section">
                  <div className="avatar-container">
                    <img 
                      src={profileForm.avatarPreview} 
                      alt="Profile avatar" 
                      className="avatar-image" 
                    />
                    <div className="avatar-overlay">
                      <label htmlFor="avatar-upload" className="avatar-upload-label">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.121-1.121A2 2 0 0011.172 3H8.828a2 2 0 00-1.414.586L6.293 4.707A1 1 0 015.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                        </svg>
                      </label>
                      <input 
                        type="file" 
                        id="avatar-upload" 
                        className="avatar-upload" 
                        accept="image/*"
                        onChange={handleAvatarChange}
                      />
                    </div>
                  </div>
                  <div className="avatar-text">
                    <h4>Profile Picture</h4>
                    <p>Click on the image to upload a new photo</p>
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">First Name</label>
                    <input 
                      type="text" 
                      id="firstName" 
                      name="firstName" 
                      value={profileForm.firstName}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="lastName">Last Name</label>
                    <input 
                      type="text" 
                      id="lastName" 
                      name="lastName" 
                      value={profileForm.lastName}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="email">Email Address</label>
                    <input 
                      type="email" 
                      id="email" 
                      name="email" 
                      value={profileForm.email}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="phone">Phone Number</label>
                    <input 
                      type="tel" 
                      id="phone" 
                      name="phone" 
                      value={profileForm.phone}
                      onChange={handleProfileChange}
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label htmlFor="company">Company Name</label>
                  <input 
                    type="text" 
                    id="company" 
                    name="company" 
                    value={profileForm.company}
                    onChange={handleProfileChange}
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="bio">Bio</label>
                  <textarea 
                    id="bio" 
                    name="bio" 
                    rows="4"
                    value={profileForm.bio}
                    onChange={handleProfileChange}
                  ></textarea>
                  <p className="input-help">Brief description for your profile.</p>
                </div>
                
                <div className="form-actions">
                  <button 
                    type="submit" 
                    className="save-button"
                    disabled={profileSubmitting}
                  >
                    {profileSubmitting ? (
                      <>
                        <span className="spinner"></span>
                        <span>Saving...</span>
                      </>
                    ) : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          )}
          
          {/* Notification Settings */}
          {activeTab === 'notifications' && (
            <div className="settings-panel">
              <h3>Notification Preferences</h3>
              <p className="panel-description">Manage how you receive notifications and updates</p>
              
              {notificationsMessage.text && (
                <div className={`message ${notificationsMessage.type}`}>
                  {notificationsMessage.type === 'success' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  )}
                  <span>{notificationsMessage.text}</span>
                </div>
              )}
              
              <form onSubmit={handleNotificationsSubmit} className="settings-form">
                <div className="notification-section">
                  <h4>Email Notifications</h4>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Email Notifications</h5>
                        <p>Receive email notifications for important updates</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.emailNotifications}
                          onChange={() => handleNotificationToggle('emailNotifications')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Order Updates</h5>
                        <p>Receive notifications when orders are placed, shipped, or delivered</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.orderUpdates}
                          onChange={() => handleNotificationToggle('orderUpdates')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Product Alerts</h5>
                        <p>Get notified about product reviews and questions</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.productAlerts}
                          onChange={() => handleNotificationToggle('productAlerts')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Inventory Alerts</h5>
                        <p>Get notified when inventory is low or out of stock</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.inventoryAlerts}
                          onChange={() => handleNotificationToggle('inventoryAlerts')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Marketing Emails</h5>
                        <p>Receive promotional emails and special offers</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.marketingEmails}
                          onChange={() => handleNotificationToggle('marketingEmails')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                </div>
                
                <div className="notification-section">
                  <h4>Other Notifications</h4>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>SMS Notifications</h5>
                        <p>Receive text messages for important updates</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.smsNotifications}
                          onChange={() => handleNotificationToggle('smsNotifications')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Browser Notifications</h5>
                        <p>Receive notifications in your browser</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          checked={notificationSettings.browserNotifications}
                          onChange={() => handleNotificationToggle('browserNotifications')}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                </div>
                
                <div className="form-actions">
                  <button 
                    type="submit" 
                    className="save-button"
                    disabled={notificationsSubmitting}
                  >
                    {notificationsSubmitting ? (
                      <>
                        <span className="spinner"></span>
                        <span>Saving...</span>
                      </>
                    ) : 'Save Preferences'}
                  </button>
                </div>
              </form>
            </div>
          )}
          
          {/* Account Settings */}
          {activeTab === 'account' && (
            <div className="settings-panel">
              <h3>Account Settings</h3>
              <p className="panel-description">Manage your account preferences and settings</p>
              
              {accountMessage.text && (
                <div className={`message ${accountMessage.type}`}>
                  {accountMessage.type === 'success' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  )}
                  <span>{accountMessage.text}</span>
                </div>
              )}
              
              <form onSubmit={handleAccountSubmit} className="settings-form">
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="language">Language</label>
                    <select 
                      id="language" 
                      name="language" 
                      value={accountSettings.language}
                      onChange={handleAccountSettingChange}
                    >
                      <option value="english">English</option>
                      <option value="spanish">Spanish</option>
                      <option value="french">French</option>
                      <option value="german">German</option>
                      <option value="chinese">Chinese</option>
                    </select>
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="timezone">Timezone</label>
                    <select 
                      id="timezone" 
                      name="timezone" 
                      value={accountSettings.timezone}
                      onChange={handleAccountSettingChange}
                    >
                      <option value="UTC-12">UTC-12:00</option>
                      <option value="UTC-11">UTC-11:00</option>
                      <option value="UTC-10">UTC-10:00</option>
                      <option value="UTC-9">UTC-09:00</option>
                      <option value="UTC-8">UTC-08:00</option>
                      <option value="UTC-7">UTC-07:00</option>
                      <option value="UTC-6">UTC-06:00</option>
                      <option value="UTC-5">UTC-05:00</option>
                      <option value="UTC-4">UTC-04:00</option>
                      <option value="UTC-3">UTC-03:00</option>
                      <option value="UTC-2">UTC-02:00</option>
                      <option value="UTC-1">UTC-01:00</option>
                      <option value="UTC+0">UTC+00:00</option>
                      <option value="UTC+1">UTC+01:00</option>
                      <option value="UTC+2">UTC+02:00</option>
                      <option value="UTC+3">UTC+03:00</option>
                      <option value="UTC+4">UTC+04:00</option>
                      <option value="UTC+5">UTC+05:00</option>
                      <option value="UTC+6">UTC+06:00</option>
                      <option value="UTC+7">UTC+07:00</option>
                      <option value="UTC+8">UTC+08:00</option>
                      <option value="UTC+9">UTC+09:00</option>
                      <option value="UTC+10">UTC+10:00</option>
                      <option value="UTC+11">UTC+11:00</option>
                      <option value="UTC+12">UTC+12:00</option>
                    </select>
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="currency">Currency</label>
                    <select 
                      id="currency" 
                      name="currency" 
                      value={accountSettings.currency}
                      onChange={handleAccountSettingChange}
                    >
                      <option value="usd">USD - US Dollar</option>
                      <option value="eur">EUR - Euro</option>
                      <option value="gbp">GBP - British Pound</option>
                      <option value="cad">CAD - Canadian Dollar</option>
                      <option value="aud">AUD - Australian Dollar</option>
                      <option value="jpy">JPY - Japanese Yen</option>
                    </select>
                  </div>
                </div>
                
                <div className="toggle-section">
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Two-Factor Authentication</h5>
                        <p>Add an extra layer of security to your account</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          name="twoFactorAuth"
                          checked={accountSettings.twoFactorAuth}
                          onChange={handleAccountSettingChange}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Auto-Save</h5>
                        <p>Automatically save changes as you make them</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          name="autoSave"
                          checked={accountSettings.autoSave}
                          onChange={handleAccountSettingChange}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                  
                  <div className="toggle-group">
                    <div className="toggle-label">
                      <div>
                        <h5>Dark Mode</h5>
                        <p>Switch between light and dark mode</p>
                      </div>
                      <label className="toggle-switch">
                        <input 
                          type="checkbox" 
                          name="darkMode"
                          checked={accountSettings.darkMode}
                          onChange={handleAccountSettingChange}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                </div>
                
                <div className="form-actions">
                  <button 
                    type="submit" 
                    className="save-button"
                    disabled={accountSubmitting}
                  >
                    {accountSubmitting ? (
                      <>
                        <span className="spinner"></span>
                        <span>Saving...</span>
                      </>
                    ) : 'Save Settings'}
                  </button>
                </div>
              </form>
            </div>
          )}
          
          {/* Security Settings */}
          {activeTab === 'security' && (
            <div className="settings-panel">
              <h3>Security Settings</h3>
              <p className="panel-description">Manage your password and security preferences</p>
              
              {passwordMessage.text && (
                <div className={`message ${passwordMessage.type}`}>
                  {passwordMessage.type === 'success' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  )}
                  <span>{passwordMessage.text}</span>
                </div>
              )}
              
              <div className="security-section">
                <h4>Change Password</h4>
                <form onSubmit={handlePasswordSubmit} className="settings-form">
                  <div className="form-group">
                    <label htmlFor="currentPassword">Current Password</label>
                    <input 
                      type="password" 
                      id="currentPassword" 
                      name="currentPassword" 
                      value={passwordForm.currentPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </div>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <label htmlFor="newPassword">New Password</label>
                      <input 
                        type="password" 
                        id="newPassword" 
                        name="newPassword" 
                        value={passwordForm.newPassword}
                        onChange={handlePasswordChange}
                        required
                      />
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="confirmPassword">Confirm New Password</label>
                      <input 
                        type="password" 
                        id="confirmPassword" 
                        name="confirmPassword" 
                        value={passwordForm.confirmPassword}
                        onChange={handlePasswordChange}
                        required
                      />
                    </div>
                  </div>
                  
                  <div className="password-requirements">
                    <h5>Password Requirements:</h5>
                    <ul>
                      <li>Minimum 8 characters</li>
                      <li>At least one uppercase letter</li>
                      <li>At least one number</li>
                      <li>At least one special character</li>
                    </ul>
                  </div>
                  
                  <div className="form-actions">
                    <button 
                      type="submit" 
                      className="save-button"
                      disabled={passwordSubmitting}
                    >
                      {passwordSubmitting ? (
                        <>
                          <span className="spinner"></span>
                          <span>Updating...</span>
                        </>
                      ) : 'Change Password'}
                    </button>
                  </div>
                </form>
              </div>
              
              <div className="security-section">
                <h4>Login Sessions</h4>
                <p>These are devices that have logged into your account</p>
                
                <div className="sessions-list">
                  <div className="session-item current">
                    <div className="session-info">
                      <div className="device-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H5V5h10v7H8.771z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div>
                        <h5>Current Session</h5>
                        <p>MacOS - Chrome Browser</p>
                        <span className="session-time">Active now</span>
                      </div>
                    </div>
                    <div className="session-actions">
                      <span className="current-badge">Current</span>
                    </div>
                  </div>
                  
                  <div className="session-item">
                    <div className="session-info">
                      <div className="device-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M7 2a2 2 0 00-2 2v12a2 2 0 002 2h6a2 2 0 002-2V4a2 2 0 00-2-2H7zm3 14a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div>
                        <h5>Mobile Device</h5>
                        <p>iOS - Safari Browser</p>
                        <span className="session-time">Last active: 2 days ago</span>
                      </div>
                    </div>
                    <div className="session-actions">
                      <button className="revoke-button">Revoke</button>
                    </div>
                  </div>
                  
                  <div className="session-item">
                    <div className="session-info">
                      <div className="device-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H5V5h10v7H8.771z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div>
                        <h5>Desktop Device</h5>
                        <p>Windows - Firefox Browser</p>
                        <span className="session-time">Last active: 1 week ago</span>
                      </div>
                    </div>
                    <div className="session-actions">
                      <button className="revoke-button">Revoke</button>
                    </div>
                  </div>
                </div>
                
                <div className="logout-all">
                  <button className="logout-all-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V4a1 1 0 00-1-1H3zm11 3a1 1 0 10-2 0v6.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L14 12.586V6z" clipRule="evenodd" />
                    </svg>
                    Log Out All Other Sessions
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SettingsManager;