import React, { ReactNode } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface LayoutProps {
  children: ReactNode;
}

// Basic Header component
const Header: React.FC = () => {
  const navigate = useNavigate();
  const { checkAuthStatus } = useAuth();

  const handleLogout = async () => {
    try {
      // Call backend logout endpoint to clear the cookie
      await axios.get('/api/auth/logout');
      // Update auth state in context
      await checkAuthStatus(); 
      // Redirect to login page
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
      // Handle logout error (e.g., show a message)
    }
  };

  return (
    <header style={{ background: 'linear-gradient(to right, #008080, #90EE90)', padding: '1rem', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h1>Instagram Audience App</h1>
      <nav style={{ display: 'flex', gap: '1rem' }}>
        <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none' }}>Dashboard</Link>
        <Link to="/audience" style={{ color: 'white', textDecoration: 'none' }}>Audience</Link>
        <Link to="/products" style={{ color: 'white', textDecoration: 'none' }}>Products</Link>
        <Link to="/reports" style={{ color: 'white', textDecoration: 'none' }}>Reports</Link>
        <Link to="/insights" style={{ color: 'white', textDecoration: 'none' }}>Insights</Link>
        <button onClick={handleLogout} style={{ background: 'none', border: '1px solid white', color: 'white', padding: '0.5rem 1rem', cursor: 'pointer' }}>
          Logout
        </button>
      </nav>
    </header>
  );
};

// Main Layout component
const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <main style={{ flexGrow: 1, padding: '1rem' }}>
        {children}
      </main>
      <footer style={{ background: '#f0f0f0', padding: '1rem', textAlign: 'center', marginTop: 'auto' }}>
        <p>© 2025 Instagram Audience App</p>
      </footer>
    </div>
  );
};

export default Layout;

