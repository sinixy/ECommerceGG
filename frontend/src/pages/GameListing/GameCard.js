import './GameListing.css';
import { useLocation, Link } from 'react-router-dom';

function GameCard({ game }) {
  const location = useLocation();

  return (
    <div className="col-xl-3 game-col">
      <div className="card">
        <div className="card-body d-flex flex-column justify-content-center">
            <h4 className="text-center card-title">{game.name}</h4>
            <div className="d-flex justify-content-center pt-1"><img src={game.icon.url} /></div>
            <div className="d-flex justify-content-center h-100">
              <div className="d-flex justify-content-center mt-auto">
                <Link
                  className="btn btn-primary rounded-0"
                  to={`${location.pathname}/game/${game.id}`}>
                  View Products <i className="fas fa-caret-right"></i>
                </Link>
              </div>
            </div>
        </div>
      </div>
    </div>
  )
}

export default GameCard;