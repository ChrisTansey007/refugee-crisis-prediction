import { useState, useEffect } from 'react';
import { 
  Users, 
  TrendingUp, 
  AlertTriangle, 
  Database,
  Map,
  Activity,
  HeartPulse
} from 'lucide-react';
import axios from 'axios';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [systemHealth, setSystemHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch ETL status for stats
      const etlResponse = await axios.get('/api/v1/etl/status');
      setStats(etlResponse.data);

      // Fetch system health
      const healthResponse = await axios.get('/api/v1/system/health');
      setSystemHealth(healthResponse.data);

      // Fetch time series data for migration trends (mock endpoint for now)
      // In a real app, this would be something like /api/v1/migration/trends
      // We'll mock some data for demonstration
      const mockChartData = [
        { name: 'Jan', displacement: 1200000 },
        { name: 'Feb', displacement: 1250000 },
        { name: 'Mar', displacement: 1300000 },
        { name: 'Apr', displacement: 1280000 },
        { name: 'May', displacement: 1350000 },
        { name: 'Jun', displacement: 1400000 },
      ];
      setChartData(mockChartData);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    await fetchDashboardData();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border-l-4 border-red-400 text-red-700">
        <h3 className="text-lg font-medium mb-2">Error Loading Dashboard</h3>
        <p>{error}</p>
        <button 
          onClick={handleRefresh}
          className="mt-4 btn btn-primary"
        >
          Retry
        </button>
      </div>
    );
  }

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
        {stats && [
          {
            name: 'Countries',
            value: stats.dimensions?.countries || 0,
            icon: Database,
            color: 'bg-blue-500',
          },
          {
            name: 'Displacement Records',
            value: stats.facts?.displacement || 0,
            icon: Users,
            color: 'bg-green-500',
          },
          {
            name: 'Conflict Events',
            value: stats.facts?.conflict || 0,
            icon: AlertTriangle,
            color: 'bg-red-500',
          },
          {
            name: 'Economic Indicators',
            value: stats.facts?.economic || 0,
            icon: TrendingUp,
            color: 'bg-purple-500',
          },
        ].map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.name}</p>
                <p className="mt-2 text-3xl font-bold text-gray-900">
                  {stat.value.toLocaleString()}
                </p>
              </div>
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and Map */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Time Series Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Migration Trends (Last 6 Months)
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="displacement" stroke="#0ea5e9" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Map Placeholder */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Global Migration Map
          </div>
          <div className="aspect-w-16 aspect-h-9 bg-gray-200 rounded-lg flex items-center justify-center">
            <div className="text-gray-500">
              <Map className="w-6 h-6 mr-2" /> Interactive Map View
            </div>
          </div>
        </div>

        {/* System Health */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            System Health
          </div>
          {systemHealth ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">API Status</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  systemHealth.apiStatus === 'healthy' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {systemHealth.apiStatus === 'healthy' ? 'Healthy' : 'Unhealthy'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Database</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  systemHealth.databaseStatus === 'connected' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {systemHealth.databaseStatus === 'connected' ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">ML Models</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  systemHealth.mlModelsStatus === 'ready' 
                    ? 'bg-blue-100 text-blue-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {systemHealth.mlModelsStatus === 'ready' ? 'Ready' : 'Not Ready'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Data Freshness</span>
                <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
                  {systemHealth.dataFreshness || 'Unknown'}
                </span>
              </div>
            </div>
          ) : (
            <div className="text-gray-500 text-center py-4">Loading system health...</div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Quick Actions
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button 
            onClick={handleRefresh}
            className="btn btn-primary"
          >
            Refresh Data
          </button>
          <button 
            className="btn btn-secondary"
          >
            Run Predictions
          </button>
          <button 
            className="btn btn-secondary"
          >
            Generate Report
          </button>
        </div>
      </div>
    </div>
  );
}