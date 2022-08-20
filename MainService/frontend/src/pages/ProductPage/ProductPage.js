import { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { UserContext, CartContext } from '../../contexts';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import TextField from '@mui/material/TextField';
import Rating from '@mui/material/Rating';
import ProductGallery from './ProductGallery';
import { Review } from '../../components';
import './ProductPage.css';

function ProductPage() {
  const { productId } = useParams();
  const { user } = useContext(UserContext);
  const { dispatchCart } = useContext(CartContext);
  const [product, setProduct] = useState({});
  const [reviews, setReviews] = useState([]);
  const [quantity, setQuantity] = useState(0);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');

  useEffect(() => {
    const fetchProduct = async () => {
      let response = await fetch(`/api/v1/product/${productId}`);
      let data = await response.json();
      if (response.status === 200) {
        setProduct(data.data.product);
        setQuantity(data.data.product.min_quantity);
      }
    }
    const fetchReviews = async () => {
      let response = await fetch(`/api/v1/review?productId=${productId}`);
      let data = await response.json();
      if (response.status === 200) setReviews(data.data.reviews);
    }

    fetchProduct().catch(console.error);
    fetchReviews().catch(console.error);
  }, []);

  const handlePostReview = async (event) => {
    let response = await fetch('/api/v1/review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': user.csrf
      },
      body: JSON.stringify({productId: parseInt(productId), rating, comment})
    });
    if (response.status === 201) {
      let data = await response.json();
      setReviews([data.data.review, ...reviews]);
    }
  }

  const handleAddToCart = async () => {
    let response = await fetch('/api/v1/cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': user.csrf
      },
      body: JSON.stringify({productId: parseInt(productId), quantity})
    })
    let data = await response.json();
    if (data.status === 'success') {
      let { item, is_new } = data.data;
      if (is_new) {
        dispatchCart({type: 'ADD_ITEM', payload: item});
      } else {
        dispatchCart({type: 'SET_ITEM_QUANTITY', payload: {itemId: item.id, quantity: item.quantity}});
      }
    }
  }

  return (
    <div className="container main-content">
      <div className="row">
        <div className="col-md-6 col-xl-4">
          { product.gallery !== undefined && (
          <ProductGallery images={product.gallery.images} />
          )}
        </div>
        <div className="col-md-6">
          <div className="product-title">
            <h1>{product.title}</h1>
          </div>
          <div>
            <Table>
              <TableBody>
                <TableRow key="price">
                  <TableCell>Price</TableCell>
                  <TableCell>${product.price}</TableCell>
                </TableRow>
                <TableRow key="min-quantity">
                  <TableCell>Min Quantity</TableCell>
                  <TableCell>{product.min_quantity}</TableCell>
                </TableRow>
                <TableRow key="in-stock">
                  <TableCell>In Stock</TableCell>
                  <TableCell>{product.available_quantity}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
            <div className="d-flex flex-column product-buy-section">
              <TextField
                type="number"
                label="Quantity"
                value={quantity}
                onChange={e => setQuantity(e.target.value)}
                inputProps={{min: product.min_quantity, max: product.available_quantity}} />
              { product.price !== undefined && (
              <button
                className="btn btn-primary buy-btn"
                type="button"
                onClick={handleAddToCart}>${(quantity * product.price).toFixed(2)} | Buy
              </button>
              )}
            </div>
          </div>
        </div>
      </div>
      <div>
        <p>{product.description}</p>
      </div>

      { user.id !== undefined ? (
        <div className="user-review-section d-flex flex-column my-5 w-50">
          <textarea
            className="form-control user-review-textarea"
            onChange={e => setComment(e.target.value)}>
          </textarea>
          <div className="d-flex flex-row">
            <Rating value={rating} onChange={(e, newRating) => setRating(newRating)} />
            <button className="btn user-review-btn ms-auto" onClick={handlePostReview}>Post</button>
          </div>
        </div>
        ) : (
        <div class="border rounded-0 border-dark d-flex justify-content-xl-center align-items-xl-center my-5 w-75">
          <p class="my-2">Log In to leave a review for this product!</p>
        </div>
      )}

      { reviews.length > 0 && (
      <ul className="d-flex flex-column review-list list-unstyled">
        {reviews.map(review => <Review key={review.id} review={review} />)}
      </ul>
      )}
    </div>
  );
}

export default ProductPage;