import React from 'react';

const Header = () => {
  return (
    <header className="bg-white shadow p-4 flex justify-between items-center">
      <h2 className="text-xl font-semibold text-navy-900">Welcome, Seller</h2>
      <button className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700">Logout</button>
    </header>
  );
};

export default Header;