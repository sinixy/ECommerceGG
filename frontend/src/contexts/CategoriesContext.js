import { createContext, useState, useEffect } from 'react';


const CategoriesContext = createContext();

export function CategoriesProvider({children}) {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      const response = await fetch('/api/v1/category', {method: 'GET'});
      if (response.status === 200) {
        const data = await response.json();
        setCategories(data.data.categories);
      }
    }
    fetchCategories().catch(console.error);
  }, [])

  return (
    <CategoriesContext.Provider value={categories}>
      {children}
    </CategoriesContext.Provider>
  );
}

export default CategoriesContext;