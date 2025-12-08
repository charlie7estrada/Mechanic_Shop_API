import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './views/Home';
import Register from './views/Register';
import Login from './views/Login';
import Profile from './views/Profile';
import Update from './views/Update';
import MechanicsList from './views/MechanicsList';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/update" element={<Update />} />
          <Route path="/mechanics" element={<MechanicsList />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;