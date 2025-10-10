import api from './axios.js';

// Restaurant booking API endpoints
export const restaurant = {
  // Table management
  getTables: (params = {}) => api.get('/restaurant-booking/tables/', { params }),
  searchTables: (searchData) => api.post('/restaurant-booking/tables/search/', searchData),
  getTableDetail: (tableId) => api.get(`/restaurant-booking/tables/${tableId}/`),
  
  // Booking management
  getBookings: (params = {}) => api.get('/restaurant-booking/bookings/', { params }),
  createBooking: (bookingData) => api.post('/restaurant-booking/bookings/create/', bookingData),
  getBookingDetail: (bookingId) => api.get(`/restaurant-booking/bookings/${bookingId}/`),
  cancelBooking: (bookingId) => api.post(`/restaurant-booking/bookings/${bookingId}/cancel/`),
  confirmBooking: (bookingId) => api.post(`/restaurant-booking/bookings/${bookingId}/confirm/`),
  searchBookingByCode: (code) => api.get('/restaurant-booking/bookings/search/', { params: { code: code } }),
  
  // Chat endpoints
  sendMessage: async (messageData) => {
    const controller = new AbortController();

    try {
      const baseURL = api.defaults?.baseURL || '';
      const response = await fetch(
        `${baseURL}/restaurant-booking/chat/stream/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(messageData),
          signal: controller.signal,
        }
      );

      if (!response.ok) {
        controller.abort();
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Stream reader for SSE
      const reader = response.body.getReader();
      return { reader, controller };
    } catch (error) {
      controller.abort();
      console.error('[Streaming Error]:', error);
      throw error;
    }
  },
};

export default restaurant;
