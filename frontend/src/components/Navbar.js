import { useContext } from 'react';
import { Link } from 'react-router-dom';
import '../assets/main.css';
import { UserContext, CategoriesContext, LoginContext, CartContext } from '../contexts';

function Navbar() {
  const categories = useContext(CategoriesContext);
  const { user, dispatchUser } = useContext(UserContext);
  const { cart, dispatchCart } = useContext(CartContext);
  const { showLogin, setShowLogin } = useContext(LoginContext);

  const logOut = async () => {
    const response = await fetch('/auth/token', {method: 'DELETE'});
    if (response.status === 200) {
      dispatchUser({type: 'LOGOUT'});
      dispatchCart({type: 'DELETE'});
    }
  }

  return (
    <nav className="navbar navbar-light navbar-expand-lg navigation-clean-button">
      <div className="container">
        <Link className="navbar-brand" to="/">E-Commerce.gg</Link><button className="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navcol-1"><span className="visually-hidden">Toggle navigation</span><span className="navbar-toggler-icon"></span></button>
        <div id="navcol-1" className="collapse navbar-collapse">
          <ul className="navbar-nav me-auto">
            {categories.map((c, i) => (
              <li key={i} className="nav-item">
                <Link className="nav-link" to={`/category/${c.id}`}>{c.name}</Link>
              </li>)
            )}
          </ul>
          { user.username !== undefined ? (
            <ul className="navbar-nav ms-auto">
              <li className="nav-item dropdown">
                <i className="nav-link far fa-user" aria-expanded="false" data-bs-toggle="dropdown"></i>
                <div className="dropdown-menu dropdown-menu-center">
                  <h6 className="dropdown-header">Welcome, {user.username}!</h6>
                  <Link className="dropdown-item" to={`/user/${user.id}`}>Profile</Link>
                  <Link className="dropdown-item" to={`/user/${user.id}`}>Settings</Link>
                  <div className="dropdown-divider"></div>
                  <button className="dropdown-item" onClick={logOut}>Log Out</button>
                </div>
              </li>
              <li className="nav-item">
                <Link className="cart-link" to="/cart">
                  { cart.items ? (
                  <i className="nav-link fas fa-shopping-cart cart-with-items" value={cart.items.length}></i>
                  ) : (
                  <i className="nav-link fas fa-shopping-cart"></i>
                  )}
                </Link>
              </li>
            </ul>
            ) : (
            <span className="navbar-text actions">
              <Link to="/sign-up" className="sign-up-btn">Sign Up</Link>
              <button
                className="btn btn-primary"
                type="button"
                onClick={() => setShowLogin(!showLogin)}>
                Log In
              </button>
            </span>
            )
          }
        </div>
      </div>
    </nav>
  )
}

export default Navbar;