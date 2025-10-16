import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import RestaurantLayout from '../components/RestaurantBooking/RestaurantLayout.jsx';
import { restaurant as restaurantApi } from '../api/index.js';
import { 
  MagnifyingGlassIcon, 
  CalendarIcon, 
  ClockIcon, 
  UsersIcon, 
  MapPinIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

const BookingSearch = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [searchCode, setSearchCode] = useState('');
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get code from URL parameters
  const code = searchParams.get('code');

  // Handle code parameter - auto-populate search field if code is present
  useEffect(() => {
    if (code) {
      console.log('Code from URL:', code);
      setSearchCode(code.toUpperCase());
      // Auto-search if code is present
      const autoSearch = async () => {
        setLoading(true);
        setError(null);
        setBooking(null);

        try {
          const response = await restaurantApi.searchBookingByCode(code.toUpperCase());
          
          if (response.data) {
            setBooking(response.data);
          } else {
            setError('No booking found with this code. Please check your booking code and try again.');
          }
        } catch (err) {
          console.error('Error searching booking:', err);
          setError('Failed to search booking. Please try again.');
        } finally {
          setLoading(false);
        }
      };

      // Small delay to ensure component is fully mounted
      const timer = setTimeout(autoSearch, 500);
      return () => clearTimeout(timer);
    }
  }, [code]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchCode.trim()) {
      setError('Please enter a booking code');
      return;
    }

    setLoading(true);
    setError(null);
    setBooking(null);

    try {
      const response = await restaurantApi.searchBookingByCode(searchCode.trim().toUpperCase());
      
      if (response.data) {
        setBooking(response.data);
      } else {
        setError('No booking found with this code. Please check your booking code and try again.');
      }
    } catch (err) {
      console.error('Error searching booking:', err);
      setError('Failed to search booking. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case 'confirmed':
      case 'đã xác nhận':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'cancelled':
      case 'đã hủy':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'pending':
      case 'chờ xác nhận':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
      case 'completed':
      case 'hoàn thành':
        return <CheckCircleIcon className="w-5 h-5 text-blue-500" />;
      case 'no_show':
      case 'không đến':
        return <XCircleIcon className="w-5 h-5 text-gray-500" />;
      default:
        return <InformationCircleIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'confirmed':
      case 'đã xác nhận':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'cancelled':
      case 'đã hủy':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'pending':
      case 'chờ xác nhận':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'completed':
      case 'hoàn thành':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'no_show':
      case 'không đến':
        return 'bg-gray-100 text-gray-800 border-gray-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (timeString) => {
    const [hours, minutes] = timeString.split(':');
    const date = new Date();
    date.setHours(parseInt(hours), parseInt(minutes));
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  return (
    <RestaurantLayout>
      <div className="bg-gradient-to-br from-blue-50 via-white to-purple-50 min-h-screen">
        <div className="p-6 pb-32">
          <div className="max-w-4xl mx-auto">
            
            {/* Header */}
            <div className="text-center mb-12">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl mb-6 shadow-lg">
                <MagnifyingGlassIcon className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                Search Your Booking
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Enter your booking code to view your reservation details and status
              </p>
              
              {/* Code indicator */}
              {code && (
                <div className="mt-4 inline-flex items-center bg-green-100 border border-green-300 rounded-lg px-4 py-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-sm font-medium text-green-800">
                    Code from URL: {code}
                  </span>
                </div>
              )}
            </div>

            {/* Search Form */}
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 mb-8">
              <form onSubmit={handleSearch} className="space-y-6">
                <div>
                  <label htmlFor="booking-code" className="block text-sm font-semibold text-gray-700 mb-2">
                    Booking Code
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="booking-code"
                      type="text"
                      value={searchCode}
                      onChange={(e) => setSearchCode(e.target.value.toUpperCase())}
                      placeholder="Enter your booking code (e.g., ABC12345)"
                      className="block w-full pl-10 pr-3 py-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
                      disabled={loading}
                    />
                  </div>
                  <p className="mt-2 text-sm text-gray-500">
                    Your booking code was provided when you made your reservation
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={loading || !searchCode.trim()}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-4 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Searching...
                    </div>
                  ) : (
                    'Search Booking'
                  )}
                </button>
              </form>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <XCircleIcon className="h-5 w-5 text-red-400" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Search Error</h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Booking Details */}
            {booking && (
              <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
                {/* Booking Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-2xl font-bold text-white">Booking Found</h2>
                      <p className="text-blue-100 mt-1">Confirmation Code: {booking.code}</p>
                    </div>
                    <div className="flex items-center">
                      {getStatusIcon(booking.status)}
                      <span className={`ml-2 px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(booking.status)}`}>
                        {booking.status}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Booking Content */}
                <div className="p-8">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    
                    {/* Booking Information */}
                    <div className="space-y-6">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Thông tin đặt bàn</h3>
                        
                        <div className="space-y-4">
                          <div className="flex items-center">
                            <CalendarIcon className="w-5 h-5 text-blue-600 mr-3" />
                            <div>
                              <p className="text-sm font-medium text-gray-500">Ngày</p>
                              <p className="text-lg font-semibold text-gray-900">{formatDate(booking.booking_date)}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center">
                            <ClockIcon className="w-5 h-5 text-green-600 mr-3" />
                            <div>
                              <p className="text-sm font-medium text-gray-500">Giờ</p>
                              <p className="text-lg font-semibold text-gray-900">{formatTime(booking.booking_time)}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center">
                            <UsersIcon className="w-5 h-5 text-purple-600 mr-3" />
                            <div>
                              <p className="text-sm font-medium text-gray-500">Số người</p>
                              <p className="text-lg font-semibold text-gray-900">{booking.party_size} {booking.party_size === 1 ? 'person' : 'people'}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center">
                            <MapPinIcon className="w-5 h-5 text-red-600 mr-3" />
                            <div>
                              <p className="text-sm font-medium text-gray-500">Table</p>
                              <p className="text-lg font-semibold text-gray-900">
                                {booking.table_type} - Tầng {booking.table_floor}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Customer Information */}
                    <div className="space-y-6">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Thông tin khách hàng</h3>
                        
                        <div className="space-y-4">
                          <div>
                            <p className="text-sm font-medium text-gray-500">Tên</p>
                            <p className="text-lg font-semibold text-gray-900">{booking.guest_name}</p>
                          </div>
                          
                          {booking.guest_email && (
                            <div>
                              <p className="text-sm font-medium text-gray-500">Email</p>
                              <p className="text-lg font-semibold text-gray-900">{booking.guest_email}</p>
                            </div>
                          )}
                          
                          {booking.guest_phone && (
                            <div>
                              <p className="text-sm font-medium text-gray-500">Số điện thoại</p>
                              <p className="text-lg font-semibold text-gray-900">{booking.guest_phone}</p>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Special Requests */}
                      {booking.notes && (
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-4">Ghi chú</h3>
                          <div className="bg-gray-50 rounded-lg py-4">
                            <p className="text-gray-700">{booking.notes}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Booking Actions */}
                  <div className="mt-8 pt-6 border-t border-gray-200">
                    <div className="flex flex-col sm:flex-row gap-4">
                      <button
                        onClick={() => navigate('/restaurant-booking')}
                        className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
                      >
                        Đặt bàn khác
                      </button>
                      
                      <button
                        onClick={() => {
                          setBooking(null);
                          setSearchCode('');
                          setError(null);
                        }}
                        className="flex-1 bg-gray-100 text-gray-700 font-semibold py-3 px-6 rounded-xl hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200"
                      >
                        Search Another Booking
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Help Section */}
            <div className="mt-12 bg-blue-50 rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-blue-900 mb-4">Need Help?</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-blue-800 mb-2">Can't find your booking code?</h4>
                  <p className="text-blue-700 text-sm">
                    Check your email confirmation or contact us at support@restaurant.com
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold text-blue-800 mb-2">Need to modify your booking?</h4>
                  <p className="text-blue-700 text-sm">
                    Contact us directly to make changes to your reservation
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </RestaurantLayout>
  );
};

export default BookingSearch;
