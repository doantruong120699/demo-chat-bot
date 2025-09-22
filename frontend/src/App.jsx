import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Home, Login } from './pages';
import { ProtectedRoute, PublicRoute } from './components';
import { AuthProvider } from './contexts/AuthContext.jsx';
import './App.css';
import './styles/style.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Public Routes */}
          <Route 
            path="/login" 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />
          
          {/* Protected Routes */}
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            } 
          />
          
          {/* Individual Chat Route */}
          <Route 
            path="/chat/:chatId" 
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            } 
          />
          
          {/* Catch all route - redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
