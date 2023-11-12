import LoginForm from './components/LoginForm';
import { HomePage, SignupPage, GameListing, ProductListing, ProductPage, CartPage, ProfilePage } from './pages';
import { UserProvider, CategoriesProvider, LoginProvider, CartProvider } from './contexts';
import { Navbar, Footer } from './components';

import {Route, Routes} from 'react-router-dom';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


function App() {
  return (
    <UserProvider>
    <CartProvider>
    <CategoriesProvider>

      <LoginProvider>
        <Navbar />
        <LoginForm />
      </LoginProvider>

      <ToastContainer
        theme="light"
        position={toast.POSITION.BOTTOM_RIGHT}
        autoClose={3000}
        style={{ width: "500px" }}
      />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sign-up" element={<SignupPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/user/:userId" element={<ProfilePage />} />
        <Route path="/category/:categoryId" element={<GameListing />} />
        <Route path="/category/:categoryId/game/:gameId" element={<ProductListing />} />
        <Route path="/category/:categoryId/game/:gameId/product/:productId" element={<ProductPage />} />
      </Routes>
      <Footer />

    </CategoriesProvider>
    </CartProvider>
    </UserProvider>
  );
}

export default App;
