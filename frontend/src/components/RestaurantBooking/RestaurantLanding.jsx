import { useNavigate } from 'react-router-dom';
import { CalendarIcon, MapPinIcon, UsersIcon, ChatBubbleLeftRightIcon, StarIcon } from '@heroicons/react/24/outline';

const RestaurantLanding = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <CalendarIcon className="w-8 h-8 text-blue-600" />,
      title: "Easy Online Booking",
      description: "Reserve your table in just a few clicks with our intuitive booking system."
    },
    {
      icon: <MapPinIcon className="w-8 h-8 text-green-600" />,
      title: "Interactive Table Selection",
      description: "Choose your perfect table from our visual restaurant floor plan."
    },
    {
      icon: <UsersIcon className="w-8 h-8 text-purple-600" />,
      title: "Flexible Group Sizes",
      description: "Accommodate any group size with our variety of table arrangements."
    },
    {
      icon: <ChatBubbleLeftRightIcon className="w-8 h-8 text-orange-600" />,
      title: "AI Assistant",
      description: "Get instant help with our intelligent chatbot for any questions."
    }
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      rating: 5,
      comment: "Amazing experience! The booking system was so easy to use and the AI assistant was incredibly helpful."
    },
    {
      name: "Michael Chen",
      rating: 5,
      comment: "The table selection feature is brilliant. I could see exactly where I'd be sitting before booking."
    },
    {
      name: "Emily Rodriguez",
      rating: 5,
      comment: "Perfect for special occasions. The chatbot helped me arrange everything for my anniversary dinner."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Welcome to PSCD
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            Experience fine dining with our AI-powered reservation system
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/restaurant-booking')}
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors shadow-lg"
            >
              Book a Table Now
            </button>
            <button
              onClick={() => navigate('/chat')}
              className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors"
            >
              Back to Chat App
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Our Booking System?
            </h2>
            <p className="text-xl text-gray-600">
              Experience the future of restaurant reservations
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="mb-4 flex justify-center">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              What Our Customers Say
            </h2>
            <p className="text-xl text-gray-600">
              Don't just take our word for it
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <StarIcon key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-4 italic">
                  "{testimonial.comment}"
                </p>
                <p className="font-semibold text-gray-900">
                  - {testimonial.name}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-blue-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Experience the Future of Dining?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Book your table today and enjoy a seamless reservation experience
          </p>
          <button
            onClick={() => navigate('/restaurant-booking')}
            className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors shadow-lg"
          >
            Start Your Reservation
          </button>
        </div>
      </div>
    </div>
  );
};

export default RestaurantLanding;
