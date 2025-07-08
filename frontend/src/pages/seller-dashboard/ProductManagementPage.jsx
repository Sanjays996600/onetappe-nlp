import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import ProductManager from '../../components/ProductManager';

/**
 * ProductManagementPage - A page component that integrates the ProductManager
 * within the dashboard layout
 */
const ProductManagementPage = () => {
  return (
    <DashboardLayout>
      <Sidebar />
      <div className="dashboard-content">
        <Header title="Product Management" />
        <div className="dashboard-main-content">
          <ProductManager />
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ProductManagementPage;