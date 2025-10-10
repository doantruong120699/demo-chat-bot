import { useNavigate } from 'react-router-dom';
import { ChatBubbleLeftRightIcon, CalendarIcon, SparklesIcon, UserGroupIcon } from '@heroicons/react/24/outline';

const WelcomeHome = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <ChatBubbleLeftRightIcon className="w-12 h-12 text-blue-600" />,
      title: "AI Chat Assistant",
      description: "Intelligent conversation with our advanced AI assistant. Get help with questions, tasks, and more.",
      route: "/chat",
      color: "blue"
    },
    {
      icon: <CalendarIcon className="w-12 h-12 text-green-600" />,
      title: "Restaurant Booking",
      description: "Book tables with our AI-powered reservation system. Interactive table selection and instant assistance.",
      route: "/restaurant-booking",
      color: "green"
    }
  ];

  const stats = [
    { label: "Active Users", value: "10,000+" },
    { label: "AI Conversations", value: "50,000+" },
    { label: "Restaurant Bookings", value: "5,000+" },
    { label: "Satisfaction Rate", value: "98%" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            {/* Logo and Title */}
            <div className="flex justify-center mb-8">
              <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
                <SparklesIcon className="w-10 h-10 text-white" />
              </div>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
              Welcome to
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                PSCD AI Assistant
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto">
              Your intelligent companion for conversations and restaurant bookings. 
              Experience the future of AI-powered assistance.
            </p>

            {/* Main Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
              <button
                onClick={() => navigate('/chat')}
                className="group bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                <div className="flex items-center justify-center">
                  <ChatBubbleLeftRightIcon className="w-6 h-6 mr-3" />
                  Start Chatting
                </div>
              </button>
              
              <button
                onClick={() => navigate('/restaurant-booking')}
                className="group bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                <div className="flex items-center justify-center">
                  <CalendarIcon className="w-6 h-6 mr-3" />
                  Book a Table
                </div>
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                    {stat.value}
                  </div>
                  <div className="text-gray-600">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Choose Your Experience
            </h2>
            <p className="text-xl text-gray-600">
              Two powerful AI-powered services at your fingertips
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {features.map((feature, index) => (
              <div
                key={index}
                onClick={() => navigate(feature.route)}
                className="group cursor-pointer bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100"
              >
                <div className="flex items-start space-x-6">
                  <div className={`p-4 rounded-xl bg-${feature.color}-50 group-hover:bg-${feature.color}-100 transition-colors`}>
                    {feature.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 mb-6 text-lg leading-relaxed">
                      {feature.description}
                    </p>
                    <div className="flex items-center text-blue-600 font-semibold group-hover:text-blue-700">
                      <span>Get Started</span>
                      <svg className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Simple steps to get started with our AI services
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Choose Your Service</h3>
              <p className="text-gray-600">
                Select between our AI Chat Assistant or Restaurant Booking system based on your needs.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-green-600">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Start Interacting</h3>
              <p className="text-gray-600">
                Begin your conversation with our AI or start booking your perfect restaurant table.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-purple-600">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Enjoy the Experience</h3>
              <p className="text-gray-600">
                Experience the power of AI assistance and seamless restaurant reservations.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Choose your preferred service and experience the future of AI assistance
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/chat')}
              className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-50 transition-colors shadow-lg"
            >
              Start Chatting Now
            </button>
            <button
              onClick={() => navigate('/restaurant-booking')}
              className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors"
            >
              Book a Table
            </button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <SparklesIcon className="w-6 h-6 text-white" />
              </div>
            </div>
            <h3 className="text-2xl font-bold mb-2">PSCD AI Assistant</h3>
            <p className="text-gray-400 mb-6">
              Your intelligent companion for conversations and restaurant bookings
            </p>
            <div className="flex justify-center space-x-6">
              <button
                onClick={() => navigate('/chat')}
                className="text-gray-400 hover:text-white transition-colors"
              >
                Chat Assistant
              </button>
              <button
                onClick={() => navigate('/restaurant-booking')}
                className="text-gray-400 hover:text-white transition-colors"
              >
                Restaurant Booking
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeHome;
