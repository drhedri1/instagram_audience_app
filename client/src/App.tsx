import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import AudiencePage from './pages/AudiencePage';
import ProductsPage from './pages/ProductsPage';
import ReportsPage from './pages/ReportsPage';
import InsightsPage from './pages/InsightsPage';
import Layout from './components/Layout'; // We will create this component
import AuthProvider, { useAuth } from './contexts/AuthContext'; // We will create this context

// Helper component to protect routes
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    // Optional: Show a loading spinner while checking auth status
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/*" // All other routes are protected and use the Layout
            element={
              <ProtectedRoute>
                <Layout>
                  <Routes> {/* Nested routes for layout content */}
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/audience" element={<AudiencePage />} />
                    <Route path="/products" element={<ProductsPage />} />
                    <Route path="/reports" element={<ReportsPage />} />
                    <Route path="/insights" element={<InsightsPage />} />
                    <Route path="/" element={<Navigate to="/dashboard" replace />} /> {/* Default route */}                  
                    {/* Add other protected routes here */}
                  </Routes>
                </Layout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

