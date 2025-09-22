import api from './axios.js';

// Auth API endpoints
export const auth = {
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  signup: (userData) => api.post('/auth/sign-up', userData),
  verifyEmail: (data) => api.post('/auth/verify-email', data),
  refreshToken: (refreshToken) => api.post('/auth/token/refresh', { refresh: refreshToken }),
  googleCallback: (data) => api.post('/auth/google/callback', data),
};

// Auth utility functions
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('access_token', token);
  } else {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};

export const getAuthToken = () => {
  return localStorage.getItem('access_token');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

export const clearAuthTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export default auth; 