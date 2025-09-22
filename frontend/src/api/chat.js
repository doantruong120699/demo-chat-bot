import api from './axios.js';

// Chat API endpoints
export const chat = {
  sendMessage: (messageData) => api.post('/chat', messageData),
  getHistory: (params) => api.get('/chat-history', { params }),
  getChatDetail: (chatId) => api.get(`/chat-history/${chatId}`),
  createDocumentEmbedding: (documentData) => api.post('/create-document-embedding', documentData),
};

export default chat; 