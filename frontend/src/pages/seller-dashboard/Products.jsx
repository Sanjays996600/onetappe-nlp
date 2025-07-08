import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from './ProductCard';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState({ show: false, type: '', message: '' });
  
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('/seller/products');
        setProducts(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Failed to load products. Please try again later.');
        setLoading(false);
      }
    };
    
    fetchProducts();
  }, []);
  
  const handleDeleteProduct = async (productId) => {
    try {
      await axios.delete(`/seller/products/${productId}`);
      
      // Update local state by removing the deleted product
      setProducts(products.filter(product => product.id !== productId));
      
      // Show success notification
      setNotification({
        show: true,
        type: 'success',
        message: 'Product deleted successfully!'
      });
      
      // Hide notification after 3 seconds
      setTimeout(() => {
        setNotification({ show: false, type: '', message: '' });
      }, 3000);
      
    } catch (err) {
      console.error('Error deleting product:', err);
      
      // Show error notification
      setNotification({
        show: true,
        type: 'error',
        message: err.response?.data?.message || 'Failed to delete product. Please try again.'
      });
      
      // Hide notification after 3 seconds
      setTimeout(() => {
        setNotification({ show: false, type: '', message: '' });
      }, 3000);
    }
  };

  return (
    <div className="p-4">
      {notification.show && (
        <div className={`mb-4 p-3 rounded relative ${notification.type === 'success' ? 'bg-green-100 border border-green-400 text-green-700' : 'bg-red-100 border border-red-400 text-red-700'}`} role="alert">
          <span className="block sm:inline">{notification.message}</span>
        </div>
      )}
      
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold">Product Management</h3>
        <Link 
          to="/seller-dashboard/add-product" 
          className="bg-teal-600 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded"
        >
          Add New Product
        </Link>
      </div>
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-600"></div>
        </div>
      ) : error ? (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      ) : products.length === 0 ? (
        <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">No products found. Add your first product!</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {products.map((product) => (
            <ProductCard 
              key={product.id} 
              id={product.id}
              name={product.name} 
              price={product.price} 
              stock={product.stock}
              onDelete={handleDeleteProduct}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Products;