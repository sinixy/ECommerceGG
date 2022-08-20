import LoginForm from './components/LoginForm';
import { HomePage, GameListing, ProductListing, ProductPage, CartPage, ProfilePage } from './pages';
import { UserProvider, CategoriesProvider, LoginProvider, CartProvider } from './contexts';
import { Navbar, Footer } from './components';
import {Route, Routes} from 'react-router-dom';

function App() {
  return (
    <UserProvider>
    <CartProvider>
    <CategoriesProvider>

      <LoginProvider>
        <Navbar />
        <LoginForm />
      </LoginProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
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
