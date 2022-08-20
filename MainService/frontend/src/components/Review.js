import '../assets/main.css';
import Rating from '@mui/material/Rating';
import Avatar from '@mui/material/Avatar';


function Review({ review }) {
  return (
    <li className="w-75">
      <div className="card">
        <div className="d-flex flex-row align-items-center card-header">
          <div className="d-flex flex-row align-items-center review-author">
            {review.author.profile_picture ? (
              <Avatar alt={review.author.username} src={review.author.profile_picture.url} />
            ) : (
              <Avatar>{review.author.username[0]}</Avatar>
            )}
            <div className="ms-2">{review.author.username}</div>
          </div>
          <div className="review-date">{review.created_at.split(' ').slice(0, 5).join(' ')}</div>
        </div>
        <div className="card-body p-3">
          <Rating value={review.rating} readOnly />
          <p className="card-text mt-2">{review.comment}</p>
        </div>
      </div>
    </li>
  );
}

export default Review;