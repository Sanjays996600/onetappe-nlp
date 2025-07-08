import React, { useState, useEffect } from 'react';
import './ReportsLanding.css';

/**
 * ReportsLanding component - A responsive landing page for generating and viewing reports
 * Features include report generation, filtering, and downloading in various formats
 */
const ReportsLanding = () => {
  // State for reports data
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // State for filters
  const [filters, setFilters] = useState({
    dateRange: 'last30days',
    reportType: 'all',
    status: 'all'
  });
  
  // State for search
  const [searchQuery, setSearchQuery] = useState('');
  
  // State for report generation
  const [generatingReport, setGeneratingReport] = useState(false);
  const [reportSuccess, setReportSuccess] = useState(null);
  
  // Sample report types
  const reportTypes = [
    { id: 'sales', name: 'Sales Report', description: 'Overview of sales performance and trends' },
    { id: 'inventory', name: 'Inventory Report', description: 'Current stock levels and inventory movements' },
    { id: 'customers', name: 'Customer Report', description: 'Customer demographics and purchase behavior' },
    { id: 'financial', name: 'Financial Report', description: 'Revenue, expenses, and profit margins' },
    { id: 'marketing', name: 'Marketing Report', description: 'Campaign performance and ROI analysis' }
  ];
  
  // Sample date ranges
  const dateRanges = [
    { id: 'today', name: 'Today' },
    { id: 'yesterday', name: 'Yesterday' },
    { id: 'last7days', name: 'Last 7 Days' },
    { id: 'last30days', name: 'Last 30 Days' },
    { id: 'thisMonth', name: 'This Month' },
    { id: 'lastMonth', name: 'Last Month' },
    { id: 'custom', name: 'Custom Range' }
  ];
  
  // Sample export formats
  const exportFormats = [
    { id: 'pdf', name: 'PDF', icon: '📄' },
    { id: 'excel', name: 'Excel', icon: '📊' },
    { id: 'csv', name: 'CSV', icon: '📝' }
  ];
  
  // Generate sample reports data
  useEffect(() => {
    const generateSampleReports = () => {
      setLoading(true);
      
      // Simulate API delay
      setTimeout(() => {
        try {
          const sampleReports = Array(15).fill().map((_, index) => {
            const reportType = reportTypes[Math.floor(Math.random() * reportTypes.length)];
            const date = new Date();
            date.setDate(date.getDate() - Math.floor(Math.random() * 30));
            
            return {
              id: `report-${index + 1}`,
              name: `${reportType.name} #${index + 1}`,
              type: reportType.id,
              typeName: reportType.name,
              date: date.toISOString(),
              formattedDate: date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
              }),
              status: Math.random() > 0.2 ? 'completed' : 'processing',
              size: `${Math.floor(Math.random() * 10) + 1}MB`,
              downloads: Math.floor(Math.random() * 50),
              format: exportFormats[Math.floor(Math.random() * exportFormats.length)].id
            };
          });
          
          setReports(sampleReports);
          setLoading(false);
        } catch (err) {
          setError('Failed to load reports. Please try again.');
          setLoading(false);
        }
      }, 1500);
    };
    
    generateSampleReports();
  }, []);
  
  // Handle filter changes
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };
  
  // Handle search input
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };
  
  // Filter reports based on current filters and search query
  const filteredReports = reports.filter(report => {
    // Filter by report type
    if (filters.reportType !== 'all' && report.type !== filters.reportType) {
      return false;
    }
    
    // Filter by status
    if (filters.status !== 'all' && report.status !== filters.status) {
      return false;
    }
    
    // Filter by search query
    if (searchQuery && !report.name.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }
    
    // Date range filtering would be implemented here with actual dates
    // For now, we'll return true for all date ranges
    return true;
  });
  
  // Handle report generation
  const handleGenerateReport = (reportTypeId) => {
    setGeneratingReport(true);
    setReportSuccess(null);
    
    // Simulate API call
    setTimeout(() => {
      setGeneratingReport(false);
      setReportSuccess(true);
      
      // Add the new report to the list
      const reportType = reportTypes.find(type => type.id === reportTypeId);
      const newReport = {
        id: `report-${reports.length + 1}`,
        name: `${reportType.name} #${reports.length + 1}`,
        type: reportType.id,
        typeName: reportType.name,
        date: new Date().toISOString(),
        formattedDate: new Date().toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric' 
        }),
        status: 'completed',
        size: `${Math.floor(Math.random() * 5) + 1}MB`,
        downloads: 0,
        format: 'pdf'
      };
      
      setReports(prev => [newReport, ...prev]);
      
      // Reset success message after 3 seconds
      setTimeout(() => {
        setReportSuccess(null);
      }, 3000);
    }, 2000);
  };
  
  // Handle report download
  const handleDownloadReport = (reportId) => {
    // In a real app, this would trigger a download
    console.log(`Downloading report ${reportId}`);
    
    // Update download count
    setReports(prev => prev.map(report => {
      if (report.id === reportId) {
        return { ...report, downloads: report.downloads + 1 };
      }
      return report;
    }));
  };
  
  return (
    <div className="reports-landing">
      {/* Header */}
      <div className="reports-header">
        <h2>Reports Dashboard</h2>
        <p>Generate, view, and download reports to analyze your business performance</p>
      </div>
      
      {/* Report Generation Section */}
      <div className="report-generation-section">
        <h3>Generate New Report</h3>
        
        {reportSuccess && (
          <div className="success-message">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Report generated successfully!</span>
          </div>
        )}
        
        <div className="report-types-grid">
          {reportTypes.map(type => (
            <div className="report-type-card" key={type.id}>
              <h4>{type.name}</h4>
              <p>{type.description}</p>
              <button 
                className="generate-button" 
                onClick={() => handleGenerateReport(type.id)}
                disabled={generatingReport}
              >
                {generatingReport ? (
                  <>
                    <span className="spinner"></span>
                    <span>Generating...</span>
                  </>
                ) : (
                  'Generate Report'
                )}
              </button>
            </div>
          ))}
        </div>
      </div>
      
      {/* Reports List Section */}
      <div className="reports-list-section">
        <div className="reports-controls">
          <h3>Your Reports</h3>
          
          <div className="reports-filters">
            <div className="filter-group">
              <label htmlFor="dateRange">Date Range:</label>
              <select 
                id="dateRange" 
                name="dateRange" 
                value={filters.dateRange}
                onChange={handleFilterChange}
              >
                {dateRanges.map(range => (
                  <option key={range.id} value={range.id}>{range.name}</option>
                ))}
              </select>
            </div>
            
            <div className="filter-group">
              <label htmlFor="reportType">Report Type:</label>
              <select 
                id="reportType" 
                name="reportType" 
                value={filters.reportType}
                onChange={handleFilterChange}
              >
                <option value="all">All Types</option>
                {reportTypes.map(type => (
                  <option key={type.id} value={type.id}>{type.name}</option>
                ))}
              </select>
            </div>
            
            <div className="filter-group">
              <label htmlFor="status">Status:</label>
              <select 
                id="status" 
                name="status" 
                value={filters.status}
                onChange={handleFilterChange}
              >
                <option value="all">All Statuses</option>
                <option value="completed">Completed</option>
                <option value="processing">Processing</option>
              </select>
            </div>
          </div>
          
          <div className="search-bar">
            <input 
              type="text" 
              placeholder="Search reports..." 
              value={searchQuery}
              onChange={handleSearchChange}
            />
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
            </svg>
          </div>
        </div>
        
        {loading ? (
          <div className="loading-state">
            <div className="spinner-large"></div>
            <p>Loading reports...</p>
          </div>
        ) : error ? (
          <div className="error-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>Try Again</button>
          </div>
        ) : filteredReports.length === 0 ? (
          <div className="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clipRule="evenodd" />
            </svg>
            <p>No reports found matching your criteria</p>
          </div>
        ) : (
          <div className="reports-table-container">
            <table className="reports-table">
              <thead>
                <tr>
                  <th>Report Name</th>
                  <th>Type</th>
                  <th>Date</th>
                  <th>Size</th>
                  <th>Status</th>
                  <th>Downloads</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredReports.map(report => (
                  <tr key={report.id}>
                    <td>{report.name}</td>
                    <td>{report.typeName}</td>
                    <td>{report.formattedDate}</td>
                    <td>{report.size}</td>
                    <td>
                      <span className={`status-badge ${report.status}`}>
                        {report.status === 'completed' ? 'Completed' : 'Processing'}
                      </span>
                    </td>
                    <td>{report.downloads}</td>
                    <td>
                      <div className="report-actions">
                        <button 
                          className="download-button"
                          onClick={() => handleDownloadReport(report.id)}
                          disabled={report.status !== 'completed'}
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                          </svg>
                          Download
                        </button>
                        <div className="format-badge">{report.format.toUpperCase()}</div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportsLanding;