import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './GameListing.css';
import GameCard from './GameCard';

function GameListing() {
  const { categoryId } = useParams();
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchGames = async () => {
      const response = await fetch(`/api/v1/game?categoryId=${categoryId}`, {method: 'GET'});
      const data = await response.json();
      if (response.status === 200) setGames(data.data.games);
    }
    fetchGames().catch(console.error);
  }, [categoryId]);

  return (
    <div className="container main-content">
      <div className="row games-list">
        {games.map(game => <GameCard key={game.id} game={game} />)}
      </div>
    </div>
  )
}

export default GameListing;