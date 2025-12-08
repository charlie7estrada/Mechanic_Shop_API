import { useState, useEffect } from 'react';

const MechanicsList = () => {
  const [mechanics, setMechanics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchMechanics();
  }, []);

  const fetchMechanics = async () => {
    try {
      const response = await fetch('http://localhost:5000/mechanics');
      const data = await response.json();

      if (response.ok) {
        setMechanics(data);
      } else {
        setMessage('Failed to load mechanics');
      }
    } catch (error) {
      setMessage('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={styles.container}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <h2>All Mechanics</h2>
      {message && <p>{message}</p>}
      
      {mechanics.length > 0 ? (
        <div style={styles.grid}>
          {mechanics.map((mechanic) => (
            <div key={mechanic.id} style={styles.card}>
              <h3>{mechanic.name}</h3>
              <p><strong>Email:</strong> {mechanic.email}</p>
              <p><strong>Phone:</strong> {mechanic.phone}</p>
              <p><strong>Salary:</strong> ${mechanic.salary}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No mechanics found</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '1.5rem',
    marginTop: '1.5rem',
  },
  card: {
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '1.5rem',
    backgroundColor: '#f9f9f9',
  },
};

export default MechanicsList;