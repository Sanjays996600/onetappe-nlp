import React, { useState } from 'react';
import Products from './Seller/Products';

const MainContent = () => {
    const [activeTab, setActiveTab] = useState('products');

    return (
        <div>
            <nav>
                <button onClick={() => setActiveTab('dashboard')}>Dashboard</button>
                <button onClick={() => setActiveTab('products')}>Products</button>
                {/* Add other tabs here */}
            </nav>
            <div>
                {activeTab === 'dashboard' && <div>Dashboard Content</div>}
                {activeTab === 'products' && <Products />}
            </div>
        </div>
    );
};

export default MainContent;