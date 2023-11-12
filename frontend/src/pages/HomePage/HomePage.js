import { useContext } from 'react';
import { CategoriesContext } from '../../contexts';
import CategoryCard from './CategoryCard';
import './HomePage.css';


function HomePage() {
  const categories = useContext(CategoriesContext);

  return (
    <div className="container main-content">
      <div className="home-page-top px-5 py-2">
        <div className="mt-5">
            <h1>Gaming E-Commerce Project</h1>
            <h2>Created by Sin Hlib</h2>
        </div>
      </div>
      <div className="px-5">
          <div className="card-group">
            {(categories !== undefined) && (
              categories.map(c => <CategoryCard key={c.id} category={c} />)
              )
            }
          </div>
      </div>
    </div>
  )
}

export default HomePage;