import { useState } from 'react';
import RestaurantHeader from './RestaurantHeader.jsx';
import BookingChatbot from './BookingChatbot.jsx';

const RestaurantLayout = ({ children }) => {
  const [showChatbot, setShowChatbot] = useState(false);

  return (
    <div className="bg-gray-50">
      {/* Restaurant Header */}
      <RestaurantHeader />
      
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
            className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg transition-all duration-200 hover:shadow-xl cursor-pointer"
            title="Chat with our AI assistant"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </button>
        )}

        {/* Back to Chat App */}
        {/* <button
          onClick={() => navigate('/chat')}
          className="bg-gray-600 hover:bg-gray-700 text-white p-4 rounded-full shadow-lg transition-all duration-200 hover:shadow-xl"
          title="Back to Chat App"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button> */}
      </div>

      {/* Chatbot Panel */}
      {showChatbot && (
        <div className="fixed inset-0 z-50">
          <BookingChatbot
            onClose={() => setShowChatbot(false)}
            restaurant={{
              name: "PSCD",
              floors: [
                {
                  id: 1,
                  name: "Ground Floor",
                  tables: [
                    { id: 1, number: "A1", capacity: 2, status: "available" },
                    { id: 2, number: "A2", capacity: 4, status: "occupied" },
                    { id: 3, number: "A3", capacity: 2, status: "available" },
                    { id: 4, number: "A4", capacity: 6, status: "reserved" },
                    { id: 5, number: "A5", capacity: 4, status: "available" },
                    { id: 6, number: "A6", capacity: 2, status: "available" },
                  ]
                },
                {
                  id: 2,
                  name: "First Floor",
                  tables: [
                    { id: 7, number: "B1", capacity: 4, status: "available" },
                    { id: 8, number: "B2", capacity: 6, status: "available" },
                    { id: 9, number: "B3", capacity: 2, status: "occupied" },
                    { id: 10, number: "B4", capacity: 8, status: "available" },
                    { id: 11, number: "B5", capacity: 4, status: "reserved" },
                  ]
                }
              ]
            }}
            selectedTable={null}
            selectedDate={new Date()}
            selectedTime=""
            partySize={2}
          />
        </div>
      )}
    </div>
  );
};

export default RestaurantLayout;
