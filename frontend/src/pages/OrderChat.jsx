import React from "react";
import { useSearchParams } from "react-router-dom";
import { OrderLayout, OrderLanding } from "../components/OrderBot";

const OrderChat = () => {
  const [searchParams] = useSearchParams();
  
  // Check if we should show the landing page
  const showLanding = searchParams.get('landing') === 'true';

  // Show landing page if requested
  if (showLanding) {
    return <OrderLanding />;
  }

  // Show main order chat interface with layout
  return (
    <OrderLayout>
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="max-w-4xl w-full">
          <div className="bg-white rounded-lg shadow-xl p-8 mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-4 text-center">
              Order Clothes with AI
            </h2>
            <p className="text-gray-600 text-center mb-6">
              Click the chat button in the bottom right corner to start ordering with our AI assistant
            </p>
            
            {/* Product showcase */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-6 text-center">
                <div className="text-6xl mb-4">👕</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">T-Shirts</h3>
                <p className="text-gray-600">Diverse styles, sizes and colors</p>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-6 text-center">
                <div className="text-6xl mb-4">👖</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Jeans</h3>
                <p className="text-gray-600">Modern style, high quality</p>
              </div>
              <div className="bg-gradient-to-br from-pink-50 to-purple-50 rounded-lg p-6 text-center">
                <div className="text-6xl mb-4">👗</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Dresses</h3>
                <p className="text-gray-600">Elegant and sophisticated designs</p>
              </div>
            </div>

            {/* Features */}
            <div className="mt-8 bg-gray-50 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
                Why Choose Us?
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <h4 className="font-semibold text-gray-900">Quick Ordering</h4>
                    <p className="text-gray-600 text-sm">Just chat with AI, no forms needed</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <h4 className="font-semibold text-gray-900">Smart Consultation</h4>
                    <p className="text-gray-600 text-sm">AI understands needs and suggests suitable products</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <h4 className="font-semibold text-gray-900">Fast Delivery</h4>
                    <p className="text-gray-600 text-sm">Receive within 2-3 days</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <svg className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <h4 className="font-semibold text-gray-900">24/7 Support</h4>
                    <p className="text-gray-600 text-sm">AI always ready to answer questions</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </OrderLayout>
  );
};

export default OrderChat;
