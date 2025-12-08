import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const Home = () => {
  const { user } = useContext(AuthContext);

  return (
    <div style={styles.container}>
      <h1>Welcome to Mechanic Shop</h1>
      {user ? (
        <p>Hello, {user.name}! You are logged in.</p>
      ) : (
        <p>Please login or register to continue.</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    textAlign: 'center',
  },
};

export default Home;