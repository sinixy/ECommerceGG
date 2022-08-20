import { useState, useContext } from 'react';
import Popup from 'reactjs-popup';
import Cookies from 'universal-cookie';
import { UserContext, CartContext, LoginContext } from '../contexts';
import '../assets/main.css';

const cookies = new Cookies();

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { user, dispatchUser } = useContext(UserContext);
  const { cart, dispatchCart } = useContext(CartContext);
  const { showLogin, setShowLogin } = useContext(LoginContext);

  const setCart = async () => {
    let response = await fetch('/api/v1/cart', {method: 'GET'});
    if (response.status === 200) {
      let data = await response.json();
      dispatchCart({type: 'CREATE', payload: {id: data.data.cart.id, items: data.data.cart.items}});
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    setShowLogin(false);
    const loginUser = async () => {
      let response = await fetch('/auth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password})
      });
      let data = await response.json();
      if (response.status === 200) {
        dispatchUser({type: 'LOGIN', payload: {...data.data.user, csrf: cookies.get('csrf_access_token')}});
        setCart().catch(console.error);
      }
    }
    loginUser().catch(console.error);
  }
  return (
    <Popup position="center center" closeOnDocumentClick open={showLogin} onClose={() => setShowLogin(false)}>
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="illustration d-flex justify-content-center my-2">
          <i className="fas fa-compass"></i>
        </div>
        <div className="mb-3">
          <input
            className="form-control"
            name="username"
            placeholder="Username"
            onChange={e => setUsername(e.target.value)} />
        </div>
        <div className="mb-3">
          <input
            className="form-control"
            type="password"
            name="password"
            placeholder="Password"
            onChange={e => setPassword(e.target.value)} />
        </div>
        <div className="mb-3">
          <button className="btn btn-primary d-block w-100" type="submit">Log In</button>
        </div>
        <div className="d-flex justify-content-center my-2">
          <a href="/sign-in">Sign In</a>
        </div>
      </form>
    </Popup>
  );
}

export default LoginForm;