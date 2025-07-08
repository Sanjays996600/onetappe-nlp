import React from 'react';
import DashboardLayout from './DashboardLayout';
import Sidebar from './Sidebar';
import Header from './Header';
import SalesAnalytics from '../../components/SalesAnalytics';

/**
 * SalesAnalyticsDashboard component for displaying the sales analytics page
 * This component integrates the SalesAnalytics component within the dashboard layout
 */
const SalesAnalyticsDashboard = () => {
  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row">
        <Sidebar />
        <div className="flex-1 max-w-screen-lg overflow-x-auto">
          <Header />
          <div className="p-4">
            <h2 className="text-xl font-bold mb-6">Sales Analytics Dashboard</h2>
            <p className="mb-6 text-gray-600">
              View your sales performance metrics and trends. Use the controls below to customize the chart display.
            </p>
            
            <SalesAnalytics />
            
            <div className="mt-8 grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold mb-4">Top Selling Products</h3>
                <div className="space-y-4">
                  {/* Sample data - would be dynamic in a real app */}
                  {[
                    { name: 'Premium T-Shirt', sales: 245, revenue: '$4,900' },
                    { name: 'Designer Jeans', sales: 187, revenue: '$7,480' },
                    { name: 'Leather Wallet', sales: 156, revenue: '$3,120' },
                    { name: 'Wireless Earbuds', sales: 134, revenue: '$6,700' },
                  ].map((product, index) => (
                    <div key={index} className="flex justify-between items-center border-b pb-2">
                      <span className="font-medium">{product.name}</span>
                      <div className="text-right">
                        <div className="text-sm text-gray-500">{product.sales} units</div>
                        <div className="font-semibold text-teal-600">{product.revenue}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold mb-4">Recent Sales Activity</h3>
                <div className="space-y-4">
                  {/* Sample data - would be dynamic in a real app */}
                  {[
                    { date: '2023-06-15', customer: 'John D.', amount: '$120.50', status: 'Completed' },
                    { date: '2023-06-14', customer: 'Sarah M.', amount: '$85.25', status: 'Processing' },
                    { date: '2023-06-14', customer: 'Robert K.', amount: '$210.75', status: 'Completed' },
                    { date: '2023-06-13', customer: 'Emily L.', amount: '$45.99', status: 'Completed' },
                  ].map((sale, index) => (
                    <div key={index} className="flex justify-between items-center border-b pb-2">
                      <div>
                        <div className="font-medium">{sale.customer}</div>
                        <div className="text-sm text-gray-500">{sale.date}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold">{sale.amount}</div>
                        <div className={`text-sm ${sale.status === 'Completed' ? 'text-green-500' : 'text-yellow-500'}`}>
                          {sale.status}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default SalesAnalyticsDashboard;