import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import ContactSupport from '../../components/ContactSupport';

const ContactSupportPage = () => {
  return (
    <DashboardLayout>
      <Sidebar />
      <div className="dashboard-content">
        <Header title="Contact Support" />
        <div className="dashboard-main-content">
          <ContactSupport />
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ContactSupportPage;