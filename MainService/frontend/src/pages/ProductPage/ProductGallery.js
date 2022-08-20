import './ProductPage.css'

function ProductGallery({ images }) {
  return (
    <div>
      <div id="carousel-1" className="carousel slide" data-bs-ride="carousel">
        <div className="carousel-inner">
          {images.map((img, i) => (
            <div className={'carousel-item' + (i===0 ? ' active' : '')}>
              <img className="w-100 d-block img-fluid product-img" src={img.url} alt="Slide Image" />
            </div>
          ))}
        </div>
        <div>
          <a className="carousel-control-prev" href="#carousel-1" role="button" data-bs-slide="prev">
            <span className="carousel-control-prev-icon" aria-hidden="true"></span>
            <span className="visually-hidden">Previous</span>
          </a>
          <a className="carousel-control-next" href="#carousel-1" role="button" data-bs-slide="next">
            <span className="carousel-control-next-icon" aria-hidden="true"></span>
            <span className="visually-hidden">Next</span>
          </a>
        </div>
      </div>
    </div>
  );
}

export default ProductGallery;