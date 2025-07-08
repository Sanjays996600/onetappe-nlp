import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import ProductCatalog from '../../components/ProductCatalog';

/**
 * ProductCatalogPage component for displaying the product catalog page
 * This component integrates the ProductCatalog component within the dashboard layout
 */
const ProductCatalogPage = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h2 className="text-xl font-bold mb-6">Product Catalog</h2>
            <p className="mb-6 text-gray-600">
              Manage and showcase your product catalog. Use the filters and search to find specific products.
            </p>
            
            <ProductCatalog />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ProductCatalogPage;