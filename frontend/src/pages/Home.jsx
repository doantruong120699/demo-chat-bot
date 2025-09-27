import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.js';
import Layout from '../components/Layout.jsx';
import Messages from '../components/Messages.jsx';
import { v4 as uuidv4 } from 'uuid';

const Home = () => {
  const navigate = useNavigate();
  const { chatId } = useParams();
  const { isAuthenticated } = useAuth();
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [selectedChatId, setSelectedChatId] = useState(null);

  // Handle URL parameter changes
  useEffect(() => {
    if (chatId) {
      handleChatSelect(chatId);
    }
    else {
      const newChatId = uuidv4();
      setSelectedChatId(newChatId);
      navigate(`/chat/${newChatId}`, { replace: true });
    }
  }, [chatId]);

  // Load chat history on component mount
  useEffect(() => {
    const initializeChat = async () => {
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        navigate('/login', { replace: true });
        return;
      }
      setIsLoadingHistory(false);
    };

    initializeChat();
  }, [navigate, isAuthenticated]);

  // Handle selecting a chat from the sidebar
  const handleChatSelect = async (chatId) => {
    console.log('handleChatSelect', chatId);
    if (chatId === selectedChatId) return; // Don't reload if same chat

    setSelectedChatId(chatId);
    
    if (!chatId) {
      const newChatId = uuidv4();
      setSelectedChatId(newChatId);
      navigate(`/chat/${newChatId}`, { replace: true });
    }
  };

  if (isLoadingHistory) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="flex items-center space-x-2">
          <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="text-gray-600">Loading chat...</span>
        </div>
      </div>
    );
  }

  return (
    <Layout
      onChatSelect={handleChatSelect}
      selectedChatId={selectedChatId}
    >
      <Messages chatId={selectedChatId} />
    </Layout>
  );
};

export default Home; 