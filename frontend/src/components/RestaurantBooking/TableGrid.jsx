import { useState } from 'react';

const TableGrid = ({ floors, selectedTable, onTableSelect, partySize }) => {
  const [activeFloor, setActiveFloor] = useState(floors[0]?.name || 'Floor 1');

  const getTableStatus = (table) => {
    // Check if table is booked (from API response)
    if (table.status === 'Booked') return 'reserved';
    if (table.status === 'Occupied') return 'occupied';
    if (table.status === 'Reserved') return 'reserved';
    if (table.status === 'Maintenance') return 'occupied';
    
    // Check if table is available for booking
    if (!table.is_available_for_booking) return 'reserved';
    
    // Check if table capacity is sufficient
    if (table.capacity < partySize) return 'too-small';
    
    return 'available';
  };

  const getTableClasses = (table) => {
    const baseClasses = "relative rounded-lg border-2 cursor-pointer transition-all duration-200 text-xs font-medium min-h-[80px] flex flex-col items-center justify-center hover:scale-105 transform";
    const status = getTableStatus(table);
    const isSelected = selectedTable?.id === table.id;

    let statusClasses = '';
    switch (status) {
      case 'available':
        statusClasses = 'bg-green-100 border-green-500 hover:bg-green-200 text-green-800 hover:shadow-md';
        break;
      case 'occupied':
        statusClasses = 'bg-red-100 border-red-500 text-red-800 cursor-not-allowed opacity-60';
        break;
      case 'reserved':
        statusClasses = 'bg-yellow-100 border-yellow-500 text-yellow-800 cursor-not-allowed opacity-60';
        break;
      case 'too-small':
        statusClasses = 'bg-gray-100 border-gray-400 text-gray-600 cursor-not-allowed opacity-50';
        break;
    }

    if (isSelected) {
      statusClasses = 'bg-blue-200 border-blue-600 text-blue-900 ring-2 ring-blue-300 shadow-lg';
    }

    return `${baseClasses} ${statusClasses}`;
  };

  const currentFloor = floors.find(floor => floor.name === activeFloor);

  return (
    <div className="space-y-4">
      {/* Floor Navigation */}
      <div className="flex space-x-2">
        {floors.map((floor) => (
          <button
            key={floor.name}
            onClick={() => setActiveFloor(floor.name)}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors cursor-pointer ${
              activeFloor === floor.name
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {floor.name}
          </button>
        ))}
      </div>

      {/* Restaurant Floor Plan - Grid Layout */}
      <div className="relative">
        <div className="bg-white rounded-lg border-2 border-gray-200 p-6">
          {/* Floor Header */}
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">{currentFloor?.name}</h3>
            <div className="text-sm text-gray-500">
              {currentFloor?.tables.filter(t => getTableStatus(t) === 'available').length} available
            </div>
          </div>

          {/* Tables Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            {currentFloor?.tables && currentFloor.tables.length > 0 ? (
              currentFloor.tables.map((table) => {
                const status = getTableStatus(table);
                const isSelectable = status === 'available';
                
                return (
                  <div
                    key={table.id}
                    className={`relative ${getTableClasses(table)}`}
                    onClick={() => isSelectable && onTableSelect(table)}
                    title={`Table ${table.id} - Capacity: ${table.capacity} - Status: ${table.status} - Type: ${table.table_type}`}
                  >
                    <div className="text-center p-2">
                      <div className="font-bold text-sm">T{table.id}</div>
                      <div className="text-xs opacity-75">{table.capacity} seats</div>
                      <div className="text-xs opacity-60 mt-1">{table.table_type}</div>
                    </div>
                    
                    {/* Status indicator */}
                    {status === 'too-small' && (
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-gray-400 rounded-full"></div>
                    )}
                    {status === 'occupied' && (
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></div>
                    )}
                    {status === 'reserved' && (
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-500 rounded-full"></div>
                    )}
                  </div>
                );
              })
            ) : (
              <div className="col-span-full text-center py-8 text-gray-500">
                <div className="text-lg font-medium mb-2">No tables available</div>
                <div className="text-sm">This floor doesn't have any tables configured.</div>
              </div>
            )}
          </div>
        </div>

        {/* Table Information */}
        {selectedTable && (
          <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-blue-900 mb-2">Selected Table</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="font-medium">Table:</span> T{selectedTable.id}
              </div>
              <div>
                <span className="font-medium">Capacity:</span> {selectedTable.capacity} people
              </div>
              <div>
                <span className="font-medium">Floor:</span> {currentFloor?.name}
              </div>
              <div>
                <span className="font-medium">Type:</span> {selectedTable.table_type}
              </div>
              <div>
                <span className="font-medium">Status:</span> 
                <span className="ml-1 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                  Available
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Table Statistics */}
      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-green-50 rounded-lg p-3">
          <div className="text-2xl font-bold text-green-600">
            {currentFloor?.tables.filter(t => getTableStatus(t) === 'available').length || 0}
          </div>
          <div className="text-sm text-green-700">Available</div>
        </div>
        <div className="bg-red-50 rounded-lg p-3">
          <div className="text-2xl font-bold text-red-600">
            {currentFloor?.tables.filter(t => getTableStatus(t) === 'occupied').length || 0}
          </div>
          <div className="text-sm text-red-700">Occupied</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-3">
          <div className="text-2xl font-bold text-yellow-600">
            {currentFloor?.tables.filter(t => getTableStatus(t) === 'reserved').length || 0}
          </div>
          <div className="text-sm text-yellow-700">Reserved</div>
        </div>
      </div>
    </div>
  );
};

export default TableGrid;
