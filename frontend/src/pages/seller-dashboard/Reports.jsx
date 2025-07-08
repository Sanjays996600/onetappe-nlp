import React, { useState } from 'react';
import axios from 'axios';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';

const Reports = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [dateRange, setDateRange] = useState('today');

  const handleGenerateReport = async () => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    
    try {
      const response = await axios.get(`/seller/orders/report?type=pdf&range=${dateRange}`, {
        responseType: 'blob',
      });
      
      // Create a blob from the PDF stream
      const file = new Blob([response.data], { type: 'application/pdf' });
      
      // Create a link element to trigger download
      const fileURL = URL.createObjectURL(file);
      const link = document.createElement('a');
      link.href = fileURL;
      
      // Set the filename based on date range
      const today = new Date();
      const formattedDate = today.toISOString().split('T')[0];
      link.download = `sales_report_${formattedDate}_${dateRange}.pdf`;
      
      // Append to body, click and remove
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000); // Hide success message after 3 seconds
    } catch (err) {
      console.error('Error generating report:', err);
      setError('Failed to generate report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-6">
            <h3 className="text-xl font-bold mb-6">Sales Reports</h3>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h4 className="text-lg font-semibold mb-4">Generate PDF Report</h4>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Date Range
                </label>
                <select
                  value={dateRange}
                  onChange={(e) => setDateRange(e.target.value)}
                  className="mt-1 block w-full md:w-1/3 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="today">Today</option>
                  <option value="this-week">This Week</option>
                  <option value="this-month">This Month</option>
                </select>
              </div>
              
              <button
                onClick={handleGenerateReport}
                disabled={loading}
                className={`px-4 py-2 rounded-md text-white font-medium ${loading ? 'bg-indigo-300' : 'bg-indigo-600 hover:bg-indigo-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                  </>
                ) : 'Generate PDF Report'}
              </button>
              
              {error && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
                  {error}
                </div>
              )}
              
              {success && (
                <div className="mt-4 p-3 bg-green-100 text-green-700 rounded-md">
                  Report generated successfully! Downloading...
                </div>
              )}
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h4 className="text-lg font-semibold mb-4">About Reports</h4>
              <p className="text-gray-600">
                Generate detailed sales reports for your business. Reports include:
              </p>
              <ul className="list-disc pl-5 mt-2 text-gray-600">
                <li>Order summaries</li>
                <li>Total sales</li>
                <li>Product performance</li>
                <li>Customer information</li>
              </ul>
              <p className="mt-3 text-gray-600">
                Reports are generated as PDF files that you can download, print, or share.
              </p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Reports;