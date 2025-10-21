import { useNavigate } from 'react-router-dom';
import { ShoppingBagIcon, SparklesIcon, TruckIcon, ChatBubbleLeftRightIcon, StarIcon } from '@heroicons/react/24/outline';

const OrderLanding = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <ShoppingBagIcon className="w-8 h-8 text-purple-600" />,
      title: "Wide Selection",
      description: "Browse through our extensive collection of trendy fashion items."
    },
    {
      icon: <SparklesIcon className="w-8 h-8 text-pink-600" />,
      title: "AI-Powered Shopping",
      description: "Get personalized recommendations from our intelligent assistant."
    },
    {
      icon: <TruckIcon className="w-8 h-8 text-blue-600" />,
      title: "Fast Delivery",
      description: "Quick and reliable shipping to your doorstep."
    },
    {
      icon: <ChatBubbleLeftRightIcon className="w-8 h-8 text-green-600" />,
      title: "24/7 Support",
      description: "Our AI chatbot is always ready to help with your orders."
    }
  ];

  const testimonials = [
    {
      name: "Anna Thompson",
      rating: 5,
      comment: "The AI assistant made shopping so easy! Found exactly what I wanted in minutes."
    },
    {
      name: "David Kim",
      rating: 5,
      comment: "Love the conversational ordering system. It's like chatting with a personal stylist."
    },
    {
      name: "Maria Garcia",
      rating: 5,
      comment: "Fast delivery and great quality. The AI chatbot helped me choose the perfect outfit!"
    }
  ];

  const productCategories = [
    { name: "Áo thun", image: "👕", count: "100+ items" },
    { name: "Quần jean", image: "👖", count: "80+ items" },
    { name: "Váy", image: "👗", count: "60+ items" },
    { name: "Giày", image: "👟", count: "50+ items" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Welcome to Fashion Shop
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-purple-100">
            Shop smarter with our AI-powered conversational ordering system
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/order-chat')}
              className="bg-white text-purple-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-purple-50 transition-colors shadow-lg"
            >
              Start Shopping with AI
            </button>
            <button
              onClick={() => navigate('/chat')}
              className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-purple-600 transition-colors"
            >
              Back to Chat App
            </button>
          </div>
        </div>
      </div>

      {/* Product Categories */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Shop by Category
            </h2>
            <p className="text-xl text-gray-600">
              Find your perfect style
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {productCategories.map((category, index) => (
              <div 
                key={index} 
                className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => navigate('/order-chat')}
              >
                <div className="text-6xl mb-4">{category.image}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {category.name}
                </h3>
                <p className="text-gray-600">{category.count}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Shop With Us?
            </h2>
            <p className="text-xl text-gray-600">
              Experience the future of online shopping
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

      {/* How It Works Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Simple, fast, and intelligent
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-600">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Chat with AI
              </h3>
              <p className="text-gray-600">
                Tell our AI assistant what you're looking for
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-600">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Confirm Details
              </h3>
              <p className="text-gray-600">
                Review your order information and make changes if needed
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-600">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Receive Your Order
              </h3>
              <p className="text-gray-600">
                Fast delivery right to your doorstep
              </p>
            </div>
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
              Join thousands of happy shoppers
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
      <div className="py-16 bg-gradient-to-r from-purple-600 to-pink-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Upgrade Your Wardrobe?
          </h2>
          <p className="text-xl text-purple-100 mb-8">
            Start shopping with our AI assistant today and discover your perfect style
          </p>
          <button
            onClick={() => navigate('/order-chat')}
            className="bg-white text-purple-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-purple-50 transition-colors shadow-lg"
          >
            Start Shopping Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default OrderLanding;
