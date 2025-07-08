import React from 'react';
import axios from 'axios';

function ReportDownload() {
  const handleDownload = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.get('/api/reports', {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Failed to download report');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Download Reports</h2>
      <button className="btn btn-primary" onClick={handleDownload}>
        Download Report
      </button>
    </div>
  );
}

export default ReportDownload;