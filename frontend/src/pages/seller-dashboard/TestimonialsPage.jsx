import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import TestimonialsLanding from '../../components/TestimonialsLanding';

/**
 * TestimonialsPage component - Container for the TestimonialsLanding component
 * Integrates the testimonials landing page within the dashboard layout
 */
const TestimonialsPage = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h2 className="text-xl font-bold mb-6">Customer Testimonials</h2>
            <TestimonialsLanding />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default TestimonialsPage;