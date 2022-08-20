import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import Avatar from '@mui/material/Avatar';
import './ProfilePage.css';

function ProfilePage() {
  const { userId } = useParams();
  const [user, setUser] = useState({});
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    const fetchUserData = async () => {
      const response = await fetch(`/api/v1/user/${userId}`, {method: 'GET'});
      if (response.status === 200) {
        const data = await response.json();
        setUser(data.data.user);
      }
    }
    fetchUserData().catch(console.error);
  }, [])

  return user.username ? (
    <div className="container main-content">
      <div className="row">
        <div className="user-secondary col-md-6 col-xl-4">
          { user.profile_picture ? (
          <Avatar
            src={user.profile_picture.url}
            variant="square"
            sx={{ width: 200, height: 'auto'}} />
          ) : (
          <Avatar
            variant="square"
            sx={{ width: 200, height: 200}}>
            {user.username[0]}
          </Avatar>
          )}
          <p className="text-muted">Joined {user.created_at.split(' ').slice(1, 4).join(' ')}</p>
        </div>
        <div className="user-main col-md-6">
          <Table>
            <TableBody>
              <TableRow key="username">
                <TableCell>Username</TableCell>
                <TableCell>{user.username}</TableCell>
              </TableRow>
              <TableRow key="email">
                <TableCell>Email</TableCell>
                <TableCell>{user.email}</TableCell>
              </TableRow>
              <TableRow key="in-stock">
                <TableCell>Country</TableCell>
                <TableCell>{user.country.name}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  ) : (
    <p>Loading...</p>
  );
}

export default ProfilePage;