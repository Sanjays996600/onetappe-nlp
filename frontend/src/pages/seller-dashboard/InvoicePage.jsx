import React from 'react';
import { useParams } from 'react-router-dom';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import InvoiceGenerator from '../../components/InvoiceGenerator';

const InvoicePage = () => {
  const { orderId } = useParams();

  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h3 className="text-lg font-bold mb-4">Invoice Generator</h3>
            <p className="mb-4">Order ID: {orderId}</p>
            
            <div className="bg-white rounded-lg shadow p-4">
              <InvoiceGenerator />
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default InvoicePage;