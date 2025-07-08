import React from 'react';

const Sidebar = ({ role }) => {
  const sellerNav = ["Dashboard", "Orders", "Inventory"];
  const adminNav = ["Users", "Reports", "Settings"];

  const navItems = role === "admin" ? adminNav : sellerNav;

  return (
    <nav>
      <ul>
        {navItems.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </nav>
  );
};

export default Sidebar;