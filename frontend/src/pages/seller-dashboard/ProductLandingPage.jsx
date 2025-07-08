import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import ProductLanding from '../../components/ProductLanding';

/**
 * ProductLandingPage - A page component that integrates the ProductLanding component
 * within the dashboard layout
 */
const ProductLandingPage = () => {
  return (
    <DashboardLayout
      sidebar={<Sidebar />}
      header={<Header />}
      content={
        <div className="p-4">
          <ProductLanding />
        </div>
      }
    />
  );
};

export default ProductLandingPage;