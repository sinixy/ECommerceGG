import './ProductListing.css';
import { useLocation, Link } from 'react-router-dom';

function ProductCard({ product }) {
  const location = useLocation();
  const productUrl = `${location.pathname}/product/${product.id}`;

  return (
    <div className="col product-col">
      <div className="card">
        <div className="card-body d-flex flex-column justify-content-center">
            <div className="d-flex justify-content-center">
              <Link to={productUrl}><img className="img-fluid w-100" src={product.gallery.images[0].url} /></Link>
            </div>
            <div className="product-info">
              <Link className="card-link" to={productUrl}>
                <h5 className="card-subtitle">{product.title}</h5>
              </Link>
              <div class="container product-footer">
                <div class="row m-0">
                  <div class="col-md-6">
                    <p className="card-text">${product.price}</p>
                    <p className="card-text">{product.available_quantity > 0 ? 'In stock' : 'Out of Stock'}</p>
                  </div>
                  <div class="col-md-6"></div>
                </div>
              </div>
            </div>
        </div>
      </div>
    </div>
  )
}

export default ProductCard;