import { useContext } from 'react';
import { UserContext, CartContext } from '../../contexts';
import CartItem from './CartItem';

function CartPage() {
  const { user } = useContext(UserContext);
  const { cart, dispatchCart } = useContext(CartContext);

  const clearCart = async () => {
    let response = await fetch('/api/v1/cart', {
      method: 'DELETE',
      headers: {
        'X-CSRF-TOKEN': user.csrf
      }
    });
    let data = await response.json();
    if (data.status === 'success') {
      dispatchCart({type: 'CLEAR_CART_ITEMS'});
    } else {
      console.log(data.message);
    }
  }

  return (
    <div className="container main-content">
      
    { cart.items ? (
      <div>
        <button className="btn btn-primary rounded-0" onClick={clearCart}>Clear Cart</button>
        <ul className="list-unstyled">
          {cart.items.map(item => <CartItem key={item.id} item={item} />)}
        </ul>
      </div>
    ) : (
      <div>Your cart is empty!</div>
    )}
    </div>
  );
}

export default CartPage;