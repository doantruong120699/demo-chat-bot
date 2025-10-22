import Conversation from './Conversation.jsx';

const Sidebar = ({
  showSidebar,
  setShowSidebar,
  onChatSelect,
  selectedChatId,
  refreshConversations,
}) => {
  if (!showSidebar) {
    return null;
  }

  return (
    <div className="sidebar bg-white border-r border-gray-200 flex flex-col w-full sm:w-72 lg:w-80 fixed lg:relative z-50 lg:z-auto h-full">
      {/* Sidebar Header */}
      <div className="p-3 sm:p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h2 className="text-base sm:text-lg font-semibold text-gray-900 truncate">Chats</h2>
          </div>
          <button
            onClick={() => setShowSidebar(false)}
            className="lg:hidden p-1 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Search */}
        <div className="mt-3">
          <div className="relative">
            <input
              type="text"
              placeholder="Search conversations..."
              className="w-full pl-10 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <svg className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>
      
      {/* New Chat Button */}
      <div className="p-3 border-b border-gray-200">
        <button
          onClick={onChatSelect ? () => {
            onChatSelect(null);
            // Close sidebar on mobile after new chat
            if (window.innerWidth < 1024) {
              setShowSidebar(false);
            }
          } : undefined}
          className="w-full flex items-center justify-center px-3 sm:px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="hidden sm:inline">New Chat</span>
          <span className="sm:hidden">New</span>
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-2 sm:p-3">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500 mb-2">Recent Conversations</h3>
            <Conversation 
              onChatSelect={onChatSelect}
              selectedChatId={selectedChatId}
              refreshTrigger={refreshConversations}
            />
        </div>
      </div>
    </div>
  );
};

export default Sidebar; 