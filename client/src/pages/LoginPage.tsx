import React from 'react';

const LoginPage: React.FC = () => {

  const handleLogin = () => {
    // Redirect the user to the backend endpoint that starts the OAuth flow
    window.location.href = '/api/auth/instagram/login';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', background: '#f0f0f0' }}>
      <h1>Instagram Audience Analysis</h1>
      <p>Please log in with your Instagram account to continue.</p>
      <button 
        onClick={handleLogin} 
        style={{
          padding: '1rem 2rem',
          fontSize: '1.2rem',
          color: 'white',
          background: 'linear-gradient(to right, #008080, #90EE90)', // Teal to Lime Green gradient
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '1rem'
        }}
      >
        Login with Instagram
      </button>
    </div>
  );
};

export default LoginPage;

