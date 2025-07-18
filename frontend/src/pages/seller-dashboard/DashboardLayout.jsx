import React from 'react';

const DashboardLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-navy-900">Seller Dashboard</h1>
      </header>
      <main>{children}</main>
    </div>
  );
};

export default DashboardLayout;