// Main API instance
export { default as api } from './axios.js';

// API modules
export { auth, setAuthToken, getAuthToken, isAuthenticated, clearAuthTokens } from './auth.js';
export { user } from './user.js';
export { chat } from './chat.js';

// Re-export default axios instance
export { default } from './axios.js'; 