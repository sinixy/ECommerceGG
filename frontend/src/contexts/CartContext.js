import { createContext, useReducer, useEffect } from 'react';

const CartContext = createContext();

function cartReducer(state, action) {
  const removeItemAndGetState = (state, pid) => {
    let newItems = state.items.filter(i => i.id !== pid);
    if (newItems.length > 0) {
      return {...state, items: newItems};
    } else {
      return {...state, items: null};
    }
  }
  switch (action.type) {
    case 'CREATE':
      return action.payload;

    case 'ADD_ITEM':
      // item = {id: id, quantity: quantity, product: {...}}
      if (state.items) {
        return {...state, items: [...state.items, action.payload]};
      } else {
        return {...state, items: [action.payload]};
      }

    case 'REMOVE_ITEM':
      return removeItemAndGetState(state, action.payload.itemId);
      
    case 'SET_ITEM_QUANTITY':
      // payload = {itemid: itemid, quantity: quantity}
      if (action.payload.quantity > 0) {
        let newItems = state.items.map(i => {
          if (i.id === action.payload.itemId) {
            return {...i, quantity: action.payload.quantity}
          }
          return i;
        });
        return {...state, items: newItems};
      } else {
        return removeItemAndGetState(state, action.payload.itemId);
      }

    case 'CLEAR_CART_ITEMS':
      return {...state, items: null};

    case 'DELETE':
      return {};

    default:
      return state;
  }
}

export function CartProvider({children}) {
  const [cart, dispatchCart] = useReducer(cartReducer, {});

  useEffect(() => {
    const fetchCart = async () => {
      const response = await fetch('/api/v1/cart', {method: 'GET'});
      if (response.status === 200) {
        const data = await response.json();
        dispatchCart({type: 'CREATE', payload: {id: data.data.cart.id, items: data.data.cart.items}});
      }
    }
    fetchCart().catch(console.error);
  }, []);
  
  const value = {cart, dispatchCart};

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}

export default CartContext;