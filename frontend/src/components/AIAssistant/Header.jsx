const Header = ({
  showSidebar,
  setShowSidebar,
  userProfile,
  handleLogout,
}) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-4 py-3 fixed top-0 main-content">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {!showSidebar && (
            <button
              onClick={() => setShowSidebar(true)}
              className="lg:hidden p-2 text-gray-500 hover:text-gray-700"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          )}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-gray-900">
                PSCD Assistant
              </h1>
              <p className="text-sm text-gray-500">
                Welcome back, {userProfile?.first_name || userProfile?.email || 'User'}!
              </p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={handleLogout}
            className="px-3 py-2 text-sm text-red-600 hover:text-red-900 hover:bg-red-50 rounded-md transition-colors"
          >
            Logout
          </button>
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-gray-700">
              {(userProfile?.first_name?.[0] || userProfile?.email?.[0] || 'U').toUpperCase()}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 