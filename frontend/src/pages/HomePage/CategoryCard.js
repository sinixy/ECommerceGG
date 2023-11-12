import './HomePage.css';
import { Link } from 'react-router-dom';

function CategoryCard({category}) {
  return (
    <div className="card border-white border rounded mx-4">
      <div className="card-body d-flex flex-column justify-content-center">
        <h4 className="text-center card-title">{category.name}</h4>
        <div className="d-flex justify-content-center pt-1"><img src={category.icon.url} /></div>
        <div className="d-flex justify-content-center h-100">
          <div className="d-flex justify-content-center mt-auto">
            <Link to={`/category/${category.id}`} className="btn btn-primary rounded-0">View Games <i className="fas fa-caret-right"></i></Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CategoryCard;