import { useState } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, GeoJSON } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

// Sample data - replace with API calls
const sampleDisplacementData = [
  { country: 'Afghanistan', lat: 33.9, lng: 67.7, displaced: 5000000, color: '#ef4444' },
  { country: 'Syria', lat: 34.8, lng: 38.9, displaced: 6700000, color: '#dc2626' },
  { country: 'Somalia', lat: 2.0, lng: 45.3, displaced: 2900000, color: '#f87171' },
  { country: 'South Sudan', lat: 6.8, lng: 31.3, displaced: 2200000, color: '#fca5a5' },
  { country: 'Yemen', lat: 15.5, lng: 48.5, displaced: 4300000, color: '#f97316' },
]

export default function MapView() {
  const [selectedLayer, setSelectedLayer] = useState('displacement')
  const [timeRange, setTimeRange] = useState('2023')

  const getMarkerRadius = (displaced) => {
    return Math.sqrt(displaced / 100000) * 5
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Map View</h2>
          <p className="mt-2 text-gray-600">
            Geographic visualization of displacement and risk factors
          </p>
        </div>
        
        <div className="flex space-x-4">
          <select
            value={selectedLayer}
            onChange={(e) => setSelectedLayer(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="displacement">Displacement</option>
            <option value="conflict">Conflict Events</option>
            <option value="climate">Climate Risk</option>
            <option value="predictions">Predictions</option>
          </select>
          
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
          </select>
        </div>
      </div>

      <div className="card p-0 overflow-hidden">
        <div style={{ height: '600px' }}>
          <MapContainer
            center={[20, 0]}
            zoom={2}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {selectedLayer === 'displacement' && sampleDisplacementData.map((location) => (
              <CircleMarker
                key={location.country}
                center={[location.lat, location.lng]}
                radius={getMarkerRadius(location.displaced)}
                fillColor={location.color}
                color="#fff"
                weight={2}
                opacity={1}
                fillOpacity={0.6}
              >
                <Popup>
                  <div className="p-2">
                    <h3 className="font-bold text-lg">{location.country}</h3>
                    <p className="text-sm text-gray-600">
                      Displaced: {location.displaced.toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-600">
                      Year: {timeRange}
                    </p>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>
      </div>

      {/* Legend */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Legend</h3>
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-red-600"></div>
            <span className="text-sm text-gray-600">High Displacement (&gt;5M)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-red-400"></div>
            <span className="text-sm text-gray-600">Medium Displacement (2-5M)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-red-200"></div>
            <span className="text-sm text-gray-600">Low Displacement (&lt;2M)</span>
          </div>
        </div>
      </div>
    </div>
  )
}
