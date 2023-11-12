import { createContext, useState } from 'react';


const LoginContext = createContext();

export function LoginProvider({children}) {
  const [showLogin, setShowLogin] = useState(false);
  const value = {showLogin, setShowLogin};

  return (
    <LoginContext.Provider value={value}>
      {children}
    </LoginContext.Provider>
  );
}

export default LoginContext;