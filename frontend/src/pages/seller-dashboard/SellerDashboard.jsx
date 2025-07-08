import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import InventoryTable from './InventoryTable';
import axios from 'axios';
import { useEffect, useState } from 'react';

const SellerDashboard = () => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const res = await axios.get('/inventory');
        setInventory(res.data);
      } catch (e) {
        console.error("Error fetching inventory", e);
      }
    };

    fetchInventory();
  }, []);

  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h3 className="text-lg font-bold mb-4">Inventory Overview</h3>
            <InventoryTable inventory={inventory} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default SellerDashboard;