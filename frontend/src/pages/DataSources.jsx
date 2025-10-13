import { useState } from 'react'
import { Database, RefreshCw, CheckCircle, XCircle, Clock } from 'lucide-react'

const dataSources = [
  {
    id: 'unhcr',
    name: 'UNHCR Refugee Statistics',
    description: 'Population data, asylum applications, and displacement statistics',
    status: 'active',
    lastUpdate: '2024-01-15',
    records: 125000,
    endpoint: '/api/v1/ingest/unhcr',
  },
  {
    id: 'worldbank',
    name: 'World Bank Indicators',
    description: 'Economic indicators including GDP, poverty, unemployment',
    status: 'active',
    lastUpdate: '2024-01-14',
    records: 89000,
    endpoint: '/api/v1/ingest/worldbank',
  },
  {
    id: 'acled',
    name: 'ACLED Conflict Data',
    description: 'Armed conflict events, battles, violence against civilians',
    status: 'active',
    lastUpdate: '2024-01-16',
    records: 450000,
    endpoint: '/api/v1/ingest/acled',
  },
  {
    id: 'nasa',
    name: 'NASA POWER Climate Data',
    description: 'Temperature, precipitation, and climate measurements',
    status: 'active',
    lastUpdate: '2024-01-15',
    records: 2100000,
    endpoint: '/api/v1/ingest/nasa-power',
  },
]

export default function DataSources() {
  const [refreshing, setRefreshing] = useState({})

  const handleRefresh = async (sourceId) => {
    setRefreshing({ ...refreshing, [sourceId]: true })
    // Simulate API call
    setTimeout(() => {
      setRefreshing({ ...refreshing, [sourceId]: false })
    }, 2000)
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-500" />
      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Data Sources</h2>
          <p className="mt-2 text-gray-600">
            Manage and monitor external data integrations
          </p>
        </div>
        
        <button className="btn btn-primary">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh All
        </button>
      </div>

      {/* Data Sources Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {dataSources.map((source) => (
          <div key={source.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-primary-100 rounded-lg">
                  <Database className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {source.name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    {source.description}
                  </p>
                </div>
              </div>
              {getStatusIcon(source.status)}
            </div>

            <div className="mt-4 grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Last Update</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {source.lastUpdate}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Records</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {source.records.toLocaleString()}
                </p>
              </div>
            </div>

            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => handleRefresh(source.id)}
                disabled={refreshing[source.id]}
                className="btn btn-secondary flex-1"
              >
                {refreshing[source.id] ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Refreshing...
                  </>
                ) : (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Refresh
                  </>
                )}
              </button>
              <button className="btn btn-secondary">
                Configure
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Ingestion Runs */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Ingestion Runs
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Source
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Records
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Started
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duration
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  UNHCR
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                    Success
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  1,250
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2024-01-15 10:30
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  45s
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  ACLED
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                    Success
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  3,450
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2024-01-16 08:15
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2m 15s
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
