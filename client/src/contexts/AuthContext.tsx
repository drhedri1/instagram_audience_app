import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import axios from 'axios'; // Assuming axios is used for API calls

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  checkAuthStatus: () => Promise<void>; // Function to re-check auth
  // Add login/logout functions if needed, though login is handled by backend redirect
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const checkAuthStatus = async () => {
    setIsLoading(true);
    try {
      // Check if the auth_token cookie exists (basic check)
      // A more robust check involves calling a backend endpoint
      await axios.get('/api/auth/check'); // Endpoint returns 200 if token is valid
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Authentication check failed:', error);
      setIsAuthenticated(false);
      // Optionally clear the cookie if the check fails definitively
      // document.cookie = "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Check authentication status when the provider mounts
    checkAuthStatus();
  }, []);

  const value = {
    isAuthenticated,
    isLoading,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;

