import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Products = () => {
    const [products, setProducts] = useState([]);
    const [formData, setFormData] = useState({ name: '', description: '', price: '', stock: '' });
    const [editingProduct, setEditingProduct] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:8000/products', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setProducts(response.data);
            } catch (error) {
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) return <p>Loading products...</p>;

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const method = editingProduct ? 'PUT' : 'POST';
        const url = editingProduct ? `/seller/products/${editingProduct.id}` : '/seller/products';
        await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(formData)
        });
        setFormData({ name: '', description: '', price: '', stock: '' });
        setEditingProduct(null);
        fetchProducts();
    };

    const handleEdit = (product) => {
        setFormData(product);
        setEditingProduct(product);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this product?')) {
            await fetch(`/seller/products/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            fetchProducts();
        }
    };

    return (
        <div>
            <h2>Product Management</h2>
            <form onSubmit={handleSubmit}>
                <input name="name" value={formData.name} onChange={handleInputChange} placeholder="Name" required />
                <input name="description" value={formData.description} onChange={handleInputChange} placeholder="Description" />
                <input name="price" value={formData.price} onChange={handleInputChange} placeholder="Price" required type="number" />
                <input name="stock" value={formData.stock} onChange={handleInputChange} placeholder="Stock" required type="number" />
                <button type="submit">{editingProduct ? 'Update' : 'Add'} Product</button>
            </form>
            <ul>
                {products.map(product => (
                    <li key={product.id}>
                        {product.name} - ${product.price} - Stock: {product.stock}
                        <button onClick={() => handleEdit(product)}>Edit</button>
                        <button onClick={() => handleDelete(product.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Products;