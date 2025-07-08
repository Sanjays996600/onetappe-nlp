import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import ContactForm from '../../components/ContactForm';

/**
 * ContactPage component - Container for the ContactForm component
 * Integrates the contact form within the dashboard layout
 */
const ContactPage = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h2 className="text-xl font-bold mb-6">Contact Support</h2>
            <ContactForm />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ContactPage;