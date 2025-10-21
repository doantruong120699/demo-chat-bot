import { useState } from 'react';
import OrderHeader from './OrderHeader.jsx';
import OrderChatbot from './OrderChatbot.jsx';

const OrderLayout = ({ children }) => {
  const [showChatbot, setShowChatbot] = useState(false);

  return (
    <div className="bg-gray-50">
      {/* Order Header */}
      <OrderHeader />
      
      {/* Main Content */}
      <main className="pt-16">
        {children}
      </main>

      {/* Floating Action Buttons */}
      <div className="fixed bottom-6 right-6 flex flex-col space-y-3 z-40">
        {/* Chat with AI Assistant - Hide when chatbot is open */}
        {!showChatbot && (
          <button
            onClick={() => setShowChatbot(!showChatbot)}
            className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-full shadow-lg transition-all duration-200 hover:shadow-xl cursor-pointer"
            title="Chat with our AI shopping assistant"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </button>
        )}
      </div>

      {/* Chatbot Panel */}
      {showChatbot && (
        <div className="fixed inset-0 z-50">
          <OrderChatbot
            onClose={() => setShowChatbot(false)}
          />
        </div>
      )}
    </div>
  );
};

export default OrderLayout;
