import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Home, Login, WelcomeHome, RestaurantBooking, BookingSearch, OrderChat } from './pages';
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
          
          {/* Welcome Home - Public */}
          <Route 
            path="/" 
            element={<WelcomeHome />} 
          />
          
          {/* Chat Routes - Protected */}
          <Route 
            path="/chat" 
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/chat/:chatId" 
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            } 
          />
          
          {/* Restaurant Booking Route - Public */}
          <Route 
            path="/restaurant-booking" 
            element={<RestaurantBooking />} 
          />

          <Route 
            path="/restaurant-booking/search" 
            element={<BookingSearch />} 
          />
           
          {/* Order Chat Route */}
          <Route 
            path="/order-chat" 
            element={
              <ProtectedRoute>
                <OrderChat />
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
