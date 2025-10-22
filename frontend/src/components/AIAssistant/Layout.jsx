import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth.js';
import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';

const Layout = ({ children, onChatSelect, selectedChatId, refreshConversations }) => {
  const { currentUser, logout } = useAuth();
  const [showSidebar, setShowSidebar] = useState(true);

  // Handle mobile sidebar behavior - keep desktop unchanged
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setShowSidebar(false);
      } else {
        setShowSidebar(true);
      }
    };

    // Set initial state
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="flex h-screen bg-gray-50 relative">
      {/* Mobile Overlay */}
      {showSidebar && (
        <div 
          className="fixed inset-0 bg-gray-200 bg-opacity-50 z-40 lg:hidden"
          onClick={() => setShowSidebar(false)}
        />
      )}

      {/* Sidebar */}
      <Sidebar
        showSidebar={showSidebar}
        setShowSidebar={setShowSidebar}
        onChatSelect={(chatId) => {
          onChatSelect(chatId);
          // Close sidebar on mobile after chat selection
          if (window.innerWidth < 1024) {
            setShowSidebar(false);
          }
        }}
        selectedChatId={selectedChatId}
        refreshConversations={refreshConversations}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <Header
          showSidebar={showSidebar}
          setShowSidebar={setShowSidebar}
          userProfile={currentUser}
          handleLogout={logout}
        />

        {/* Main Content */}
        <div className="flex-1 overflow-hidden">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout; 