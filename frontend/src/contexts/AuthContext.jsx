import { createContext, useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth, setAuthToken, getAuthToken, isAuthenticated, clearAuthTokens } from '../api/auth.js';
import { user } from '../api/user.js';

// Create the context
const AuthContext = createContext();

// Auth Provider component
export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticatedState, setIsAuthenticatedState] = useState(false);

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        if (isAuthenticated()) {
          // Try to get user profile
          const response = await user.getProfile();
          setCurrentUser(response.data);
          setIsAuthenticatedState(true);
        }
      } catch (error) {
        console.error('Failed to initialize auth:', error);
        // If getting profile fails, clear tokens (they might be invalid)
        logout();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = useCallback(async (credentials) => {
    try {
      setLoading(true);
      const response = await auth.login(credentials);
      const { access_token, refresh_token } = response.data.data;
      
      // Store tokens
      setAuthToken(access_token);
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token);
      }
      
      // Get user profile
      const profileResponse = await user.getProfile();
      setCurrentUser(profileResponse.data);
      setIsAuthenticatedState(true);
      
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Login failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Login failed' 
      };
    } finally {
      setLoading(false);
    }
  }, []);

  // Signup function
  const signup = useCallback(async (userData) => {
    try {
      setLoading(true);
      const response = await auth.signup(userData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Signup failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Signup failed' 
      };
    } finally {
      setLoading(false);
    }
  }, []);

  // Logout function
  const logout = useCallback(() => {
    try {
      // Call logout API (optional, for server-side cleanup)
      auth.logout().catch(error => {
        console.error('Logout API call failed:', error);
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local state and tokens
      clearAuthTokens();
      setCurrentUser(null);
      setIsAuthenticatedState(false);
      navigate('/login', { replace: true });
    }
  }, [navigate]);

  // Refresh token function
  const refreshToken = useCallback(async () => {
    try {
      const refreshTokenValue = localStorage.getItem('refresh_token');
      if (!refreshTokenValue) {
        throw new Error('No refresh token available');
      }

      const response = await auth.refreshToken(refreshTokenValue);
      const { access_token } = response.data;
      
      setAuthToken(access_token);
      return { success: true, access_token };
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      return { success: false, error: 'Token refresh failed' };
    }
  }, [logout]);

  // Update user profile
  const updateProfile = useCallback(async (userData) => {
    try {
      setLoading(true);
      const response = await user.updateProfile(userData);
      setCurrentUser(response.data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Profile update failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Profile update failed' 
      };
    } finally {
      setLoading(false);
    }
  }, []);

  // Change password
  const changePassword = useCallback(async (passwordData) => {
    try {
      setLoading(true);
      const response = await user.changePassword(passwordData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Password change failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Password change failed' 
      };
    } finally {
      setLoading(false);
    }
  }, []);

  // Verify email
  const verifyEmail = useCallback(async (data) => {
    try {
      setLoading(true);
      const response = await auth.verifyEmail(data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Email verification failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Email verification failed' 
      };
    } finally {
      setLoading(false);
    }
  }, []);

  // Google callback
  const googleCallback = useCallback(async (data) => {
    try {
      setLoading(true);
      const response = await auth.googleCallback(data);
      
      const { access_token, refresh_token } = response.data;
      
      // Store tokens
      setAuthToken(access_token);
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token);
      }
      
      // Get user profile
      const profileResponse = await user.getProfile();
      setCurrentUser(profileResponse.data);
      setIsAuthenticatedState(true);
      
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Google callback failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Google authentication failed' 
      };
    } finally {
      setLoading(false);
    }
  }, []);

  // Check if user is authenticated
  const checkAuth = useCallback(() => {
    return isAuthenticatedState && !!currentUser;
  }, [isAuthenticatedState, currentUser]);

  // Get current token
  const getToken = useCallback(() => {
    return getAuthToken();
  }, []);

  // Context value
  const value = {
    // State
    currentUser,
    loading,
    isAuthenticated: isAuthenticatedState,
    
    // Functions
    login,
    logout,
    signup,
    refreshToken,
    updateProfile,
    changePassword,
    verifyEmail,
    googleCallback,
    checkAuth,
    getToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext; 