import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Profile = () => {
  const [mechanic, setMechanic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  
  const { token, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }

    fetchProfile();
  }, [token]);

  const fetchProfile = async () => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const mechanicId = payload.sub;

      const response = await fetch(`http://localhost:5000/mechanics/${mechanicId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setMechanic(data);
      } else {
        setMessage('Failed to load profile');
      }
    } catch (error) {
      setMessage('Error loading profile');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete your account?')) {
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const mechanicId = payload.sub;

      const response = await fetch(`http://localhost:5000/mechanics/${mechanicId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        alert('Account deleted successfully');
        logout();
        navigate('/');
      } else {
        setMessage('Failed to delete account');
      }
    } catch (error) {
      setMessage('Error deleting account');
    }
  };

  if (loading) {
    return <div style={styles.container}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <h2>My Profile</h2>
      {mechanic ? (
        <div style={styles.profileCard}>
          <p><strong>Name:</strong> {mechanic.name}</p>
          <p><strong>Email:</strong> {mechanic.email}</p>
          <p><strong>Phone:</strong> {mechanic.phone}</p>
          <p><strong>Salary:</strong> ${mechanic.salary}</p>
          
          <div style={styles.buttons}>
            <button 
              onClick={() => navigate('/update')} 
              style={styles.updateBtn}
            >
              Update Profile
            </button>
            <button 
              onClick={handleDelete} 
              style={styles.deleteBtn}
            >
              Delete Account
            </button>
          </div>
        </div>
      ) : (
        <p>{message}</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '600px',
    margin: '2rem auto',
    padding: '2rem',
  },
  profileCard: {
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '1.5rem',
    backgroundColor: '#f9f9f9',
  },
  buttons: {
    marginTop: '1.5rem',
    display: 'flex',
    gap: '1rem',
  },
  updateBtn: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  deleteBtn: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
};

export default Profile;