import React from 'react';

const InventoryTable = ({ inventory }) => {
  return (
    <table className="min-w-full bg-white">
      <thead>
        <tr>
          <th className="py-2 px-4 bg-gray-200">Product Name</th>
          <th className="py-2 px-4 bg-gray-200">Stock Level</th>
          <th className="py-2 px-4 bg-gray-200">Low Stock Warning</th>
        </tr>
      </thead>
      <tbody>
        {inventory.map((item, index) => (
          <tr key={index} className="border-b">
            <td className="py-2 px-4">{item.name}</td>
            <td className="py-2 px-4">{item.stock}</td>
            <td className="py-2 px-4">
              {item.stock < 5 ? (
                <span className="text-red-500">Low Stock</span>
              ) : (
                <span className="text-green-600">In Stock</span>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default InventoryTable;