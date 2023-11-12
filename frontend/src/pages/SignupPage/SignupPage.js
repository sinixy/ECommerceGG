import { useState, useEffect } from 'react';
import Select from 'react-select';
import { toast } from 'react-toastify';


function SignupPage() {
 const [countries, setCountries] = useState([]);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [countryId, setCountryId] = useState(0);

  useEffect(() => {
    const fetchCountries = async () => {
      const response = await fetch('/api/v1/country', {method: 'GET'});
      if (response.status === 200) {
        const data = await response.json();
        setCountries(data.data.countries);
      }
    }
    fetchCountries().catch(console.error);
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    const signup = async () => {
      let response = await fetch('/api/v1/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password, email, countryId})
      });
      let data = await response.json();
      if (data.status === 'success') {
        toast.success('You can now log in!')
      } else {
        if (data.message) {
          console.log('yes')
          toast.error(data.message);
        } else {
          console.log('no')
          toast.error(Object.values(data.data).join('\n'));
        }
      }
    }
    signup().catch(console.error);
  }

  return (
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-6 offset-md-3">
          <h2 class="text-center">Sign Up</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label for="username">Username</label>
              <input
                type="text"
                className="form-control"
                id="username"
                onChange={e => setUsername(e.target.value)}
                required />
            </div>
            <div className="form-group">
              <label for="password">Password</label>
              <input
                type="password"
                className="form-control"
                id="password"
                onChange={e => setPassword(e.target.value)}
                required />
            </div>
            <div className="form-group">
              <label for="email">Email</label>
              <input
                type="email"
                className="form-control"
                id="email"
                onChange={e => setEmail(e.target.value)}
                required />
            </div>
            <div className="form-group">
              <label for="country">Country</label>
              <Select
                id="country"
                placeholder="Choose a country..."
                onChange={e => setCountryId(e.value)}
                options={ countries.map(c => ({value: c.id, label: c.name})) }
              />
            </div>
            <button type="submit" className="btn btn-primary w-100">Sign Up</button>
          </form>
        </div>
      </div>
  </div>

  );
}

export default SignupPage;