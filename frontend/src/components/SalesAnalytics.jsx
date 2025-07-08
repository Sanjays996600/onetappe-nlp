import React, { useState, useEffect } from 'react';
import SalesChart from './SalesChart';
import './SalesAnalytics.css';

/**
 * SalesAnalytics component for displaying sales data analytics
 * This component provides a responsive dashboard with various chart types
 * and filtering options for sales data visualization
 */
const SalesAnalytics = () => {
  const [salesData, setSalesData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartType, setChartType] = useState('bar');
  const [timeRange, setTimeRange] = useState('week');
  
  // Sample data - in a real app, this would come from an API
  const generateSampleData = (range) => {
    let labels = [];
    let data = [];
    
    if (range === 'day') {
      labels = ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM'];
      data = [12, 19, 15, 25, 22, 30, 28, 25, 18];
    } else if (range === 'week') {
      labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      data = [65, 59, 80, 81, 56, 95, 40];
    } else if (range === 'month') {
      labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
      data = [300, 450, 320, 500];
    } else if (range === 'year') {
      labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      data = [540, 480, 590, 620, 560, 550, 640, 610, 580, 630, 670, 720];
    }
    
    return {
      labels,
      datasets: [{
        label: 'Sales',
        data,
        backgroundColor: labels.map((_, i) => `rgba(66, 153, 225, ${0.6 + (i * 0.05)})`),
        borderColor: '#2b6cb0',
        borderWidth: 1
      }]
    };
  };
  
  // Fetch data based on selected time range
  useEffect(() => {
    setIsLoading(true);
    
    // Simulate API call with setTimeout
    setTimeout(() => {
      try {
        const data = generateSampleData(timeRange);
        setSalesData(data);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to load sales data');
        setIsLoading(false);
      }
    }, 500);
    
    // In a real application, you would fetch from an API:
    // fetch('/api/sales-data?timeRange=' + timeRange)
    //   .then(response => response.json())
    //   .then(data => {
    //     setSalesData(data);
    //     setIsLoading(false);
    //   })
    //   .catch(err => {
    //     setError('Failed to load sales data');
    //     setIsLoading(false);
    //   });
  }, [timeRange]);
  
  // Calculate summary statistics
  const calculateStats = () => {
    if (!salesData) return { total: 0, average: 0, highest: 0 };
    
    const values = salesData.datasets[0].data;
    const total = values.reduce((sum, val) => sum + val, 0);
    const average = Math.round(total / values.length);
    const highest = Math.max(...values);
    
    return { total, average, highest };
  };
  
  const stats = calculateStats();
  
  if (error) {
    return <div className="sales-analytics-error">Error: {error}</div>;
  }
  
  return (
    <div className="sales-analytics-container">
      <div className="sales-analytics-header">
        <h2>Sales Analytics</h2>
        
        <div className="sales-analytics-controls">
          <div className="chart-type-selector">
            <label htmlFor="chart-type">Chart Type:</label>
            <select 
              id="chart-type" 
              value={chartType} 
              onChange={(e) => setChartType(e.target.value)}
            >
              <option value="bar">Bar Chart</option>
              <option value="line">Line Chart</option>
              <option value="pie">Pie Chart</option>
            </select>
          </div>
          
          <div className="time-range-selector">
            <label htmlFor="time-range">Time Range:</label>
            <select 
              id="time-range" 
              value={timeRange} 
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <option value="day">Today</option>
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="year">This Year</option>
            </select>
          </div>
        </div>
      </div>
      
      <div className="sales-analytics-summary">
        <div className="summary-card">
          <h3>Total Sales</h3>
          <p className="summary-value">${stats.total}</p>
        </div>
        <div className="summary-card">
          <h3>Average Sales</h3>
          <p className="summary-value">${stats.average}</p>
        </div>
        <div className="summary-card">
          <h3>Highest Sales</h3>
          <p className="summary-value">${stats.highest}</p>
        </div>
      </div>
      
      <div className="sales-chart-wrapper">
        {isLoading ? (
          <div className="loading-spinner">
            <svg viewBox="0 0 50 50" className="spinner">
              <circle cx="25" cy="25" r="20" fill="none" strokeWidth="5"></circle>
            </svg>
            <p>Loading chart data...</p>
          </div>
        ) : (
          <SalesChart 
            data={salesData} 
            type={chartType} 
            height={400} 
            width="100%" 
          />
        )}
      </div>
    </div>
  );
};

export default SalesAnalytics;