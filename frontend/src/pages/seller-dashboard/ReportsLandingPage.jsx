import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import ReportsLanding from '../../components/ReportsLanding';

/**
 * ReportsLandingPage component - Container for the ReportsLanding component
 * Integrates the reports landing page within the dashboard layout
 */
const ReportsLandingPage = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <ReportsLanding />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ReportsLandingPage;