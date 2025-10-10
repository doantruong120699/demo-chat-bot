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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 overflow-hidden">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
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
                PSCD AI Assistant Demo
              </span>
            </h1>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="pb-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><script type="module" src=""></script>
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
