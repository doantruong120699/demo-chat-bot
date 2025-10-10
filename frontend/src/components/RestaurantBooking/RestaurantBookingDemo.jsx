import { useNavigate } from 'react-router-dom';
import { CalendarIcon, MapPinIcon, UsersIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

const RestaurantBookingDemo = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <CalendarIcon className="w-8 h-8 text-blue-600" />,
      title: "Easy Booking",
      description: "Select your preferred date and time with our intuitive calendar interface."
    },
    {
      icon: <MapPinIcon className="w-8 h-8 text-green-600" />,
      title: "Table Selection",
      description: "Choose your perfect table from our interactive restaurant floor plan."
    },
    {
      icon: <UsersIcon className="w-8 h-8 text-purple-600" />,
      title: "Party Management",
      description: "Accommodate any group size with our flexible table arrangements."
    },
    {
      icon: <ChatBubbleLeftRightIcon className="w-8 h-8 text-orange-600" />,
      title: "AI Assistant",
      description: "Get instant help with our intelligent chatbot for any questions."
    }
  ];

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Our Restaurant Booking System
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Experience seamless table reservations with our beautiful, AI-powered booking platform
        </p>
        <button
          onClick={() => navigate('/restaurant-booking')}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg text-lg transition-colors shadow-lg hover:shadow-xl"
        >
          Start Booking Now
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {features.map((feature, index) => (
          <div key={index} className="bg-white rounded-lg p-6 shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex flex-col items-center text-center">
              <div className="mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Ready to Make a Reservation?
        </h2>
        <p className="text-gray-600 mb-6">
          Our AI assistant is ready to help you find the perfect table for your dining experience.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/restaurant-booking')}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Book a Table
          </button>
          <button
            onClick={() => navigate('/chat')}
            className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Back to Chat
          </button>
        </div>
      </div>
    </div>
  );
};

export default RestaurantBookingDemo;
