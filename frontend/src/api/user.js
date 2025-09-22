import api from './axios.js';

// User API endpoints
export const user = {
  getProfile: () => api.get('/account/me'),
  updateProfile: (userData) => api.put('/account/update', userData),
  changePassword: (passwordData) => api.post('/account/change-password', passwordData),
};

export default user; 