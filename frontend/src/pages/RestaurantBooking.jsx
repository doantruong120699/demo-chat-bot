import { useState, useEffect, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import RestaurantLayout from '../components/RestaurantBooking/RestaurantLayout.jsx';
import RestaurantLanding from '../components/RestaurantBooking/RestaurantLanding.jsx';
import BookingForm from '../components/RestaurantBooking/BookingForm.jsx';
import TableGrid from '../components/RestaurantBooking/TableGrid.jsx';
import BookingChatbot from '../components/RestaurantBooking/BookingChatbot.jsx';
import { restaurant as restaurantApi } from '../api/index.js';
import { CalendarIcon, ClockIcon, UsersIcon, MapPinIcon, BookOpenIcon } from '@heroicons/react/24/outline';

const RestaurantBooking = () => {
  const [searchParams] = useSearchParams();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedTime, setSelectedTime] = useState('');
  const [partySize, setPartySize] = useState(2);
  const [selectedTable, setSelectedTable] = useState(null);
  const [showChatbot, setShowChatbot] = useState(false);
  const [, setTables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dateLoading, setDateLoading] = useState(false);

  // Check if we should show the landing page or booking interface
  const showLanding = searchParams.get('landing') === 'true';

  // Restaurant data
  const restaurant = useMemo(() => ({
    name: "PSCD",
    floors: [] // Will be populated from API
  }), []);

  // Fetch tables from API with date filter
  useEffect(() => {
    const fetchTables = async () => {
      try {
        setLoading(true);
        setDateLoading(true);
        const dateStr = selectedDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
        const response = await restaurantApi.getTables({ date: dateStr });

        // The API now returns an array of floors, each with a tables array
        // Example: [{ name: "Floor 1", tables: [...] }, { name: "Floor 2", tables: [...] }]
        const apiFloors = response.data;

        // Map API floors to component format
        restaurant.floors = apiFloors.map((floor, idx) => ({
          id: idx + 1,
          name: floor.name,
          tables: floor.tables.map(table => ({
            ...table,
            number: `T${table.id}`,
            // Normalize status to lower-case English for TableGrid logic
            status: (() => {
              // Map Vietnamese status to English
              const statusMap = {
                "Có sẵn": "available",
                "Đã đặt": "reserved",
                "Đang sử dụng": "occupied",
                "Bảo trì": "maintenance",
                "Reserved": "reserved",
                "Occupied": "occupied",
                "Available": "available",
                "Maintenance": "maintenance"
              };
              return statusMap[table.status] || table.status.toLowerCase();
            })()
          }))
        }));

        setTables(
          apiFloors.flatMap(floor => floor.tables)
        );
        setError(null);
      } catch (err) {
        console.error('Error fetching tables:', err);
        setError('Failed to load tables. Please try again.');
      } finally {
        setLoading(false);
        setDateLoading(false);
      }
    };

    fetchTables();
  }, [restaurant, selectedDate]);

  const timeSlots = [
    "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM",
    "2:00 PM", "2:30 PM", "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM",
    "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM", "9:30 PM"
  ];

  const handleTableSelect = (table) => {
    if (table.status === 'available') {
      setSelectedTable(table);
    }
  };

  const handleBookingSubmit = async (formData) => {
    try {
      if (!selectedTable) {
        alert('Please select a table first.');
        return;
      }

      const bookingData = {
        table_id: selectedTable.id,
        customer_name: formData.customerName,
        customer_phone: formData.phone,
        customer_email: formData.email,
        party_size: partySize,
        booking_date: selectedDate.toISOString().split('T')[0],
        booking_time: selectedTime,
        duration_hours: 2, // Default 2 hours
      };

      console.log('Submitting booking:', bookingData);
      
      const response = await restaurantApi.createBooking(bookingData);
      
      if (response.data.success) {
        alert('Booking confirmed! We will contact you shortly.');
        // Reset form
        setSelectedTable(null);
        setSelectedTime('');
        setPartySize(2);
      } else {
        alert('Failed to create booking. Please try again.');
      }
    } catch (error) {
      console.error('Error creating booking:', error);
      alert('Failed to create booking. Please try again.');
    }
  };

  // Show landing page if requested
  if (showLanding) {
    return <RestaurantLanding />;
  }

  return (
    <RestaurantLayout>
      <div className="bg-gradient-to-br from-blue-50 via-white to-purple-50 min-h-screen">
        {/* Main Booking Area */}
        <div className="p-6 pb-32">
          <div className="max-w-7xl mx-auto">
            
            {/* Loading State */}
            {loading && (
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading tables...</p>
                </div>
              </div>
            )}

            {/* Error State */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Error loading tables</h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Content - only show if not loading */}
            {!loading && (
              <>
                {/* Header */}
                <div className="text-center mb-12">
                  {/* <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl mb-6 shadow-lg">
                    <BookOpenIcon className="w-8 h-8 text-white" />
                  </div> */}
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    {restaurant.name}
                  </h1>
                  <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                    Select your preferred table and time for an unforgettable dining experience
                  </p>
                </div>

                {/* Restaurant Info Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                  <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
                        <CalendarIcon className="h-6 w-6 text-blue-600" />
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-900 mb-1">Date</p>
                        <p className="text-sm text-gray-600">
                          {selectedDate.toLocaleDateString('en-US', { 
                            weekday: 'short', 
                            month: 'short', 
                            day: 'numeric' 
                          })}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mr-4">
                        <ClockIcon className="h-6 w-6 text-green-600" />
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-900 mb-1">Time</p>
                        <p className="text-sm text-gray-600">
                          {selectedTime || 'Select time'}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mr-4">
                        <UsersIcon className="h-6 w-6 text-purple-600" />
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-900 mb-1">Party Size</p>
                        <p className="text-sm text-gray-600">{partySize} people</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center mr-4">
                        <MapPinIcon className="h-6 w-6 text-red-600" />
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-900 mb-1">Location</p>
                        <p className="text-sm text-gray-600">Downtown</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Date Filter Section */}
                <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6 mb-8">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center mr-4">
                        <CalendarIcon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h2 className="text-xl font-bold text-gray-900">Filter by Date</h2>
                        <p className="text-sm text-gray-600">Select a date to see table availability</p>
                      </div>
                    </div>
                    
                    {/* Date Display */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2">
                      <div className="flex items-center">
                        <CalendarIcon className="w-4 h-4 text-blue-600 mr-2" />
                        <span className="text-sm font-medium text-blue-800">
                          {selectedDate.toLocaleDateString('en-US', { 
                            weekday: 'long', 
                            year: 'numeric', 
                            month: 'long', 
                            day: 'numeric' 
                          })}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Date Picker */}
                  <div className="flex items-center space-x-4">
                    <div className="flex-1">
                      <label htmlFor="date-picker" className="block text-sm font-medium text-gray-700 mb-2">
                        Select Date
                      </label>
                      <input
                        id="date-picker"
                        type="date"
                        value={selectedDate.toISOString().split('T')[0]}
                        onChange={(e) => setSelectedDate(new Date(e.target.value))}
                        min={new Date().toISOString().split('T')[0]} // Can't select past dates
                        disabled={dateLoading}
                        className={`w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm transition-all duration-200 hover:border-blue-400 ${
                          dateLoading ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                      />
                    </div>
                    
                    {/* Quick Date Buttons */}
                    <div className="flex flex-col space-y-2">
                      <button
                        onClick={() => setSelectedDate(new Date())}
                        disabled={dateLoading}
                        className={`px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
                          selectedDate.toDateString() === new Date().toDateString()
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        } ${dateLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                      >
                        Today
                      </button>
                      <button
                        onClick={() => {
                          const tomorrow = new Date();
                          tomorrow.setDate(tomorrow.getDate() + 1);
                          setSelectedDate(tomorrow);
                        }}
                        disabled={dateLoading}
                        className={`px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
                          selectedDate.toDateString() === new Date(Date.now() + 24 * 60 * 60 * 1000).toDateString()
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        } ${dateLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                      >
                        Tomorrow
                      </button>
                    </div>
                  </div>

                  {/* Date Info */}
                  <div className="mt-4 p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                        <span className="text-gray-700">Available tables for this date</span>
                      </div>
                      <div className="text-gray-600">
                        {dateLoading ? (
                          <div className="flex items-center">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                            Loading...
                          </div>
                        ) : (
                          `${restaurant.floors.reduce((total, floor) => 
                            total + (floor.tables?.filter(t => t.status === 'available' || t.status === 'Available').length || 0), 0
                          )} tables available`
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Table Selection */}
                  <div className="lg:col-span-2">
                    <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
                      {/* Header with Instructions */}
                      <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center">
                          <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center mr-4">
                            <UsersIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h2 className="text-2xl font-bold text-gray-900">Select Your Table</h2>
                            <p className="text-sm text-gray-600 mt-1">Choose a table that fits your party size</p>
                          </div>
                        </div>
                        
                        {/* Party Size Indicator */}
                        <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2">
                          <div className="flex items-center">
                            <UsersIcon className="w-4 h-4 text-blue-600 mr-2" />
                            <span className="text-sm font-medium text-blue-800">
                              {partySize} {partySize === 1 ? 'person' : 'people'}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Step-by-step Instructions */}
                      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-4 mb-2">
                        <div className="flex items-start">
                          <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                            <span className="text-white text-xs font-bold">1</span>
                          </div>
                          <div>
                            <h3 className="text-sm font-semibold text-blue-900 mb-1">How to select your table:</h3>
                            <div className="text-sm text-blue-800 space-y-1">
                              <p>• <strong>Green tables</strong> are available for your party size</p>
                              <p>• <strong>Click on a green table</strong> to select it</p>
                              <p>• <strong>Red tables</strong> are currently occupied</p>
                              <p>• <strong>Yellow tables</strong> are reserved by other guests</p>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Table Grid with Better Container */}
                      <div className="mb-8">
                        <div className="flex items-center justify-between mb-4">
                          {/* <h3 className="text-lg font-semibold text-gray-900">Available Tables</h3> */}
                          {selectedTable && (
                            <div className="bg-green-100 border border-green-300 rounded-lg px-3 py-1">
                              <span className="text-sm font-medium text-green-800">
                                ✓ Selected: Table {selectedTable.number}
                              </span>
                            </div>
                          )}
                        </div>
                        
                        <TableGrid
                          floors={restaurant.floors}
                          selectedTable={selectedTable}
                          onTableSelect={handleTableSelect}
                          partySize={partySize}
                        />
                      </div>

                      {/* Enhanced Table Legend */}
                      <div className="bg-gray-50 rounded-xl p-4">
                        <h3 className="text-sm font-semibold text-gray-900 mb-4 flex items-center">
                          <div className="w-4 h-4 bg-gray-400 rounded-full mr-2"></div>
                          Table Status Guide
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                          <div className="flex items-center bg-white rounded-lg p-3 border border-green-200">
                            <div className="w-6 h-6 bg-green-100 border-2 border-green-500 rounded-lg mr-3 flex-shrink-0"></div>
                            <div>
                              <span className="font-semibold text-green-800">Available</span>
                              <p className="text-green-600 text-xs">Ready to book</p>
                            </div>
                          </div>
                          <div className="flex items-center bg-white rounded-lg p-3 border border-red-200">
                            <div className="w-6 h-6 bg-red-100 border-2 border-red-500 rounded-lg mr-3 flex-shrink-0"></div>
                            <div>
                              <span className="font-semibold text-red-800">Occupied</span>
                              <p className="text-red-600 text-xs">Currently in use</p>
                            </div>
                          </div>
                          <div className="flex items-center bg-white rounded-lg p-3 border border-yellow-200">
                            <div className="w-6 h-6 bg-yellow-100 border-2 border-yellow-500 rounded-lg mr-3 flex-shrink-0"></div>
                            <div>
                              <span className="font-semibold text-yellow-800">Reserved</span>
                              <p className="text-yellow-600 text-xs">Booked by others</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Booking Form */}
                  <div className="lg:col-span-1">
                    <div className="sticky top-6">
                      <BookingForm
                        selectedTable={selectedTable}
                        selectedDate={selectedDate}
                        selectedTime={selectedTime}
                        partySize={partySize}
                        timeSlots={timeSlots}
                        onDateChange={setSelectedDate}
                        onTimeChange={setSelectedTime}
                        onPartySizeChange={setPartySize}
                        onSubmit={handleBookingSubmit}
                      />
                    </div>
                  </div>
                </div>

                {/* Chatbot Panel */}
                {showChatbot && (
                  <BookingChatbot
                    onClose={() => setShowChatbot(false)}
                    restaurant={restaurant}
                    selectedTable={selectedTable}
                    selectedDate={selectedDate}
                    selectedTime={selectedTime}
                    partySize={partySize}
                  />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </RestaurantLayout>
  );
};

export default RestaurantBooking;
