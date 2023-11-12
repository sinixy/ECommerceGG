import '../assets/main.css';


function Footer() {
  return (
    <footer className="footer-dark py-3">
      <div className="container">
        <div className="row">
          <div className="col-sm-6 col-md-3 item">
            <h3>Services</h3>
            <ul>
              <li><a href="/">Web design</a></li>
              <li><a href="/">Development</a></li>
              <li><a href="/">Hosting</a></li>
            </ul>
          </div>
          <div className="col-sm-6 col-md-3 item">
            <h3>About</h3>
            <ul>
              <li><a href="/">Company</a></li>
              <li><a href="/">Team</a></li>
              <li><a href="/">Careers</a></li>
            </ul>
          </div>
          <div className="col d-lg-flex justify-content-lg-center align-items-lg-center item social">
            <a href="/"><i className="icon ion-social-facebook"></i></a><a href="/"><i className="icon ion-social-twitter"></i></a><a href="/"><i className="icon ion-social-snapchat"></i></a><a href="/"><i className="icon ion-social-instagram"></i></a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer;