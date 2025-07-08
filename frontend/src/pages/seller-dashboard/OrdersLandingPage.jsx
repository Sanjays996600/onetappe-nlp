import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import OrdersLanding from '../../components/OrdersLanding';

/**
 * OrdersLandingPage component - Container for the OrdersLanding component
 * Integrates the orders landing page within the dashboard layout
 */
const OrdersLandingPage = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h2 className="text-xl font-bold mb-6">Orders Management</h2>
            <OrdersLanding />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default OrdersLandingPage;