import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth.js';
import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';

const Layout = ({ children, onChatSelect, selectedChatId, refreshConversations }) => {
  const { currentUser, logout } = useAuth();
  const [showSidebar, setShowSidebar] = useState(true);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        showSidebar={showSidebar}
        setShowSidebar={setShowSidebar}
        onChatSelect={onChatSelect}
        selectedChatId={selectedChatId}
        refreshConversations={refreshConversations}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <Header
          showSidebar={showSidebar}
          setShowSidebar={setShowSidebar}
          userProfile={currentUser}
          handleLogout={logout}
        />

        {/* Main Content */}
        {children}
      </div>
    </div>
  );
};

export default Layout; 