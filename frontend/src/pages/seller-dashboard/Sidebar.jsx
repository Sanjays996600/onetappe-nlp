import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <nav className="w-64 bg-white shadow-md p-4">
      <ul className="space-y-4">
        <li>
          <NavLink to="/seller-dashboard" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Dashboard Home
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/overview" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Inventory Overview
          </NavLink>
        </li>
        <li className="space-y-2">
          <NavLink to="/seller-dashboard/products" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Product Management
          </NavLink>
          <div className="pl-4">
            <NavLink to="/seller-dashboard/add-product" className={({ isActive }) => isActive ? 'font-bold text-teal-600 text-sm' : 'text-gray-600 text-sm'}>
              + Add New Product
            </NavLink>
          </div>
        </li>
        <li>
          <NavLink to="/seller-dashboard/catalog" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Product Catalog
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/orders" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Orders
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/reports" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Reports Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/analytics" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Sales Analytics
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/inventory" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Inventory
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/command-console" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Command Console
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/settings" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Settings
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/contact" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Contact Support
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/testimonials" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Testimonials
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/faq" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            FAQ
          </NavLink>
        </li>
        <li>
          <NavLink to="/seller-dashboard/support" className={({ isActive }) => isActive ? 'font-bold text-teal-600' : 'text-gray-700'}>
            Advanced Support
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Sidebar;