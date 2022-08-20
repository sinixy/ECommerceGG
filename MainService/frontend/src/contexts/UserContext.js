import { createContext, useReducer, useEffect } from 'react';
import Cookies from 'universal-cookie';

const UserContext = createContext();
const cookies = new Cookies();

function userReducer(state, action) {
  switch (action.type) {
    case 'LOGIN':
      return action.payload;

    case 'LOGOUT':
      return {};

    default:
      return state;
  }
}

export function UserProvider({children}) {
  const [user, dispatchUser] = useReducer(userReducer, {});

  useEffect(() => {
    const fetchUserData = async () => {
      const response = await fetch('/auth/token', {method: 'GET'});
      if (response.status === 200) {
        const data = await response.json();
        dispatchUser({type: 'LOGIN', payload: {...data.data.user, csrf: cookies.get('csrf_access_token')}});
      }
    }
    fetchUserData().catch(console.error);
  }, []);
  
  const value = {user, dispatchUser};

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export default UserContext;