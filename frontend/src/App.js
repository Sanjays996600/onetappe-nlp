import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SellerDashboard from './pages/seller-dashboard/SellerDashboard';
import Products from './pages/seller-dashboard/Products';
import Inventory from './pages/seller-dashboard/Inventory';
import SettingsPage from './pages/seller-dashboard/SettingsPage';
import Orders from './pages/seller-dashboard/Orders';
import AddProduct from './pages/seller-dashboard/AddProduct';
import EditProduct from './pages/seller-dashboard/EditProduct';
import Reports from './pages/seller-dashboard/Reports';
import CommandConsole from './pages/seller-dashboard/CommandConsole';
import InvoicePage from './pages/seller-dashboard/InvoicePage';
import SalesAnalyticsDashboard from './pages/seller-dashboard/SalesAnalyticsDashboard';
import ProductCatalogPage from './pages/seller-dashboard/ProductCatalogPage';
import DashboardHome from './pages/seller-dashboard/DashboardHome';
import OrdersLandingPage from './pages/seller-dashboard/OrdersLandingPage';
import ContactPage from './pages/seller-dashboard/ContactPage';
import TestimonialsPage from './pages/seller-dashboard/TestimonialsPage';
import FAQPage from './pages/seller-dashboard/FAQPage';
import ContactSupportPage from './pages/seller-dashboard/ContactSupportPage';
import ReportsLandingPage from './pages/seller-dashboard/ReportsLandingPage';
import ProductManagementPage from './pages/seller-dashboard/ProductManagementPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/seller-dashboard" replace />} />
          <Route path="/seller-dashboard" element={<DashboardHome />} />
          <Route path="/seller-dashboard/overview" element={<SellerDashboard />} />
          <Route path="/seller-dashboard/products" element={<ProductManagementPage />} />
          <Route path="/seller-dashboard/products-legacy" element={<Products />} />
          <Route path="/seller-dashboard/catalog" element={<ProductCatalogPage />} />
          <Route path="/seller-dashboard/inventory" element={<Inventory />} />
          <Route path="/seller-dashboard/orders" element={<OrdersLandingPage />} />
          <Route path="/seller-dashboard/orders-legacy" element={<Orders />} />
          <Route path="/seller-dashboard/reports" element={<ReportsLandingPage />} />
          <Route path="/seller-dashboard/reports-legacy" element={<Reports />} />
          <Route path="/seller-dashboard/analytics" element={<SalesAnalyticsDashboard />} />
          <Route path="/seller-dashboard/settings" element={<SettingsPage />} />
          <Route path="/seller-dashboard/contact" element={<ContactPage />} />
          <Route path="/seller-dashboard/testimonials" element={<TestimonialsPage />} />
          <Route path="/seller-dashboard/faq" element={<FAQPage />} />
          <Route path="/seller-dashboard/support" element={<ContactSupportPage />} />
          <Route path="/seller-dashboard/add-product" element={<AddProduct />} />
          <Route path="/seller-dashboard/edit-product/:productId" element={<EditProduct />} />
          <Route path="/seller-dashboard/command-console" element={<CommandConsole />} />
          <Route path="/invoice/:orderId" element={<InvoicePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;