import { useState, useEffect, useContext, useRef } from 'react';
import { Link } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import CircularProgress from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import './CartPage.css';
import { UserContext, CartContext } from '../../contexts';

function CartItem({ item }) {
  const product = item.product;
  const { category_id, game_id } = item.product.category_game;
  const productLink = `/category/${category_id}/game/${game_id}/product/${product.id}`;

  const [quantity, setQuantity] = useState(item.quantity);
  const [updatingQuantity, setUpdatingQuantity] = useState(false);
  const [openAlert, setOpenAlert] = useState(false);
  const { user } = useContext(UserContext);
  const { dispatchCart } = useContext(CartContext);
  const firstRender = useRef(true);

  const handleChangeQuantity = (event) => {
    if (event.target.value.length > 0) {
      let val = parseInt(event.target.value);
      if (val > product.available_quantity) {
        setQuantity(product.available_quantity);
      } else if (val < product.min_quantity) {
        setQuantity(product.min_quantity);
      } else {
        setQuantity(val);
      }
    } else {
      setQuantity(product.min_quantity);
    }
  }

  const removeItem = async () => {
    let payload = {itemId: item.id};
    let response = await fetch('/api/v1/cart', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': user.csrf
      },
      body: JSON.stringify(payload)
    });
    let data = await response.json();
    if (data.status === 'success') {
      dispatchCart({type: 'REMOVE_ITEM', payload: payload});
    } else if (data.status === 'fail') {
      console.log(data);
      setOpenAlert(true);
    } else {
      console.log(data.message);
      setOpenAlert(true);
    }
  }

  useEffect(() => {
    const handleSetQuantity = async () => {
      setUpdatingQuantity(true);
      let payload = {itemId: item.id, quantity: quantity};
      let response = await fetch('/api/v1/cart', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': user.csrf
        },
        body: JSON.stringify(payload)
      });
      let data = await response.json();
      if (data.status === 'success') {
        dispatchCart({type: 'SET_ITEM_QUANTITY', payload: payload});
      } else if (data.status === 'fail') {
        console.log(data);
        setOpenAlert(true);
      } else {
        console.log(data.message);
        setOpenAlert(true);
      }
      setUpdatingQuantity(false);
    }

    if (firstRender.current) {
      firstRender.current = false;
    } else {
      const timeoutId = setTimeout(handleSetQuantity, 1000);
      return () => clearTimeout(timeoutId);
    }
  }, [quantity]);

  const handleCloseAlert = (event, reason) => {
    console.log(reason);
    setOpenAlert(false);
  };

  return (
    <li>
      <div className="d-flex flex-column cart-product">
        <div className="d-flex cart-product-main">
          <img className="img-fluid img-product" src={product.gallery.images[0].url} alt={product.title} />
          <Link to={productLink}>{product.title}</Link>
          <i className="fas fa-times" onClick={removeItem}></i>
        </div>
        <div className="d-flex cart-product-footer">
          { updatingQuantity ? (
          <CircularProgress color="success" />
          ) : (
          <TextField
            type="number"
            label="Quantity"
            size="small"
            value={quantity}
            onChange={handleChangeQuantity}
            inputProps={{min: product.min_quantity, max: product.available_quantity}} />
          )}
          <p className="cart-item-price">${(quantity * product.price).toFixed(2)}</p>
        </div>
        <Snackbar open={openAlert} autoHideDuration={5000} onClose={handleCloseAlert}>
          <Alert severity="error" onClose={handleCloseAlert}>
            Error!
          </Alert>
        </Snackbar>
      </div>
    </li>
  );
}

export default CartItem;