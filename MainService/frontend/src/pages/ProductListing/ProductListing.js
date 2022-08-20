import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './ProductListing.css';
import ProductCard from './ProductCard';

function ProductListing() {
  const { categoryId, gameId } = useParams();
  const [products, setProducts] = useState([]);
  const [query, setQuery] = useState('');
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(999999999);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch(
      `/api/v1/product?q=${query}&categoryId=${categoryId}&gameId=${gameId}&minPrice=${minPrice}&maxPrice=${maxPrice}`,
      {method: 'GET'}
    );
    const data = await response.json();
    if (response.status === 200) setProducts(data.data.products);
  }

  useEffect(() => {
    const fetchProducts = async () => {
      const response = await fetch(`/api/v1/product?categoryId=${categoryId}&gameId=${gameId}`, {method: 'GET'});
      const data = await response.json();
      if (response.status === 200) setProducts(data.data.products);
    }
    fetchProducts().catch(console.error);
  }, []);

  return (
    <div className="container main-content">
      <form className="products-search" onSubmit={handleSubmit}>
        <div className="input-group">
          <input className="form-control shadow-none" type="text" onChange={e => setQuery(e.target.value)} />
          <button className="btn btn-primary" type="submit">Search</button>
        </div>
        <div className="d-flex mt-3 price-input-group">
          <input
            className="border rounded price-input"
            type="number"
            placeholder="min price"
            min="0"
            onChange={e => setMinPrice(e.target.value)} />
          <input
            className="border rounded price-input"
            type="number"
            placeholder="max price"
            min="0"
            onChange={e => setMaxPrice(e.target.value)} />
        </div>
      </form>

      <div className="row products-list">
        {products.map(product => <ProductCard product={product} />)}
      </div>
    </div>
  )
}

export default ProductListing;