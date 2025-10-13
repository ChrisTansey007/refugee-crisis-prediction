import { useState, useEffect } from 'react'
import { 
  Users, 
  TrendingUp, 
  AlertTriangle, 
  Database 
} from 'lucide-react'
import axios from 'axios'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch ETL status
      const etlResponse = await axios.get('/api/v1/etl/status')
      setStats(etlResponse.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    )
  }

  const statCards = [
    {
      name: 'Countries',
      value: stats?.dimensions?.countries || 0,
      icon: Database,
      color: 'bg-blue-500',
    },
    {
      name: 'Displacement Records',
      value: stats?.facts?.displacement || 0,
      icon: Users,
      color: 'bg-green-500',
    },
    {
      name: 'Conflict Events',
      value: stats?.facts?.conflict || 0,
      icon: AlertTriangle,
      color: 'bg-red-500',
    },
    {
      name: 'Economic Indicators',
      value: stats?.facts?.economic || 0,
      icon: TrendingUp,
      color: 'bg-purple-500',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="mt-2 text-gray-600">
          Overview of the Migration Forecasting System
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.name}</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">
                    {stat.value.toLocaleString()}
                  </p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Data Sources Overview */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Data Sources Status
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={[
                { name: 'Displacement', records: stats?.facts?.displacement || 0 },
                { name: 'Economic', records: stats?.facts?.economic || 0 },
                { name: 'Conflict', records: stats?.facts?.conflict || 0 },
                { name: 'Climate', records: stats?.facts?.climate || 0 },
              ]}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="records" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* System Health */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            System Health
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">API Status</span>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                Healthy
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Database</span>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                Connected
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">ML Models</span>
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                Ready
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Data Freshness</span>
              <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
                24h ago
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn btn-primary">
            Refresh Data
          </button>
          <button className="btn btn-secondary">
            Run Predictions
          </button>
          <button className="btn btn-secondary">
            Generate Report
          </button>
        </div>
      </div>
    </div>
  )
}
