import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ConfirmationModal from '../../components/ConfirmationModal';

const ProductCard = ({ id, name, price, stock, onDelete }) => {  
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  
  const handleDelete = () => {
    setShowDeleteModal(true);
  };
  
  const confirmDelete = () => {
    onDelete(id);
    setShowDeleteModal(false);
  };
  
  return (
  <div className="p-4 rounded-xl shadow bg-white">
    <h3 className="text-lg font-bold">{name}</h3>
    <p>₹{price}</p>
    <p className={stock < 5 ? "text-red-500" : "text-green-600"}>
      {stock} in stock
    </p>
    <div className="mt-4 flex justify-end space-x-2">
      <Link 
        to={`/seller-dashboard/edit-product/${id}`}
        className="bg-teal-600 hover:bg-teal-700 text-white text-sm py-1 px-3 rounded"
      >
        Edit
      </Link>
      <button
        onClick={handleDelete}
        className="bg-red-600 hover:bg-red-700 text-white text-sm py-1 px-3 rounded"
      >
        🗑️ Delete
      </button>
      
      <ConfirmationModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={confirmDelete}
        title="Delete Product"
        message={`Are you sure you want to delete ${name}? This action cannot be undone.`}
      />
    </div>
  </div>
  );
};

export default ProductCard;