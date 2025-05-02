import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Product {
  id: number;
  name: string;
  description: string | null;
  image_url: string | null;
  product_url: string | null;
}

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get<Product[]>('/api/products/');
        setProducts(response.data);
      } catch (err: any) {
        console.error("Error fetching products:", err);
        setError(err.response?.data?.error || err.message || "Failed to fetch products");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div>
      <h2>Matched Products</h2>
      <p>Based on your audience data, here are some potentially relevant products:</p>
      {loading && <p>Loading products...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {products.length > 0 ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1rem' }}>
          {products.map((product) => (
            <div key={product.id} style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '5px' }}>
              {product.image_url && <img src={product.image_url} alt={product.name} style={{ maxWidth: '100%', height: 'auto', marginBottom: '0.5rem' }} />}
              <h3>{product.name}</h3>
              {product.description && <p>{product.description}</p>}
              {product.product_url && <a href={product.product_url} target="_blank" rel="noopener noreferrer">View Product</a>}
            </div>
          ))}
        </div>
      ) : (
        !loading && !error && <p>No products found or matched.</p>
      )}
    </div>
  );
};

export default ProductsPage;

