import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import FAQSection from '../../components/FAQSection';

/**
 * FAQPage component - Container for the FAQSection component
 * Integrates the FAQ section within the dashboard layout
 */
const FAQPage = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h2 className="text-xl font-bold mb-6">Frequently Asked Questions</h2>
            <FAQSection />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default FAQPage;