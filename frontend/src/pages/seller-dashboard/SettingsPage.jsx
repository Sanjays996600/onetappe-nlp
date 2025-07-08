import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import SettingsManager from '../../components/SettingsManager';

/**
 * SettingsPage component - Integrates the SettingsManager within the dashboard layout
 */
const SettingsPage = () => {
  return (
    <DashboardLayout>
      <Sidebar />
      <div className="dashboard-content">
        <Header title="Settings" />
        <div className="dashboard-main-content">
          <SettingsManager />
        </div>
      </div>
    </DashboardLayout>
  );
};

export default SettingsPage;