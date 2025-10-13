import { TrendingUp } from 'lucide-react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts'

const samplePredictions = [
  { month: 'Jan 2024', actual: 450000, predicted: 445000, lower: 420000, upper: 470000 },
  { month: 'Feb 2024', actual: 460000, predicted: 458000, lower: 430000, upper: 486000 },
  { month: 'Mar 2024', actual: 475000, predicted: 472000, lower: 445000, upper: 499000 },
  { month: 'Apr 2024', actual: null, predicted: 485000, lower: 455000, upper: 515000 },
  { month: 'May 2024', actual: null, predicted: 495000, lower: 462000, upper: 528000 },
  { month: 'Jun 2024', actual: null, predicted: 502000, lower: 468000, upper: 536000 },
]

export default function Predictions() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Predictions</h2>
          <p className="mt-2 text-gray-600">
            View and analyze displacement forecasts
          </p>
        </div>
        
        <button className="btn btn-primary">
          Generate New Prediction
        </button>
      </div>

      {/* Prediction Chart */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          6-Month Displacement Forecast - Afghanistan
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={samplePredictions}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="upper"
              stackId="1"
              stroke="#93c5fd"
              fill="#dbeafe"
              name="Upper Bound"
            />
            <Area
              type="monotone"
              dataKey="lower"
              stackId="1"
              stroke="#93c5fd"
              fill="#ffffff"
              name="Lower Bound"
            />
            <Line
              type="monotone"
              dataKey="actual"
              stroke="#10b981"
              strokeWidth={2}
              name="Actual"
              dot={{ r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="predicted"
              stroke="#0ea5e9"
              strokeWidth={2}
              name="Predicted"
              strokeDasharray="5 5"
              dot={{ r: 4 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Prediction Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Next Month Forecast</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">
                485K
              </p>
              <p className="mt-1 text-sm text-gray-500">
                ±30K (95% CI)
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div>
            <p className="text-sm text-gray-600">Model Confidence</p>
            <p className="mt-2 text-3xl font-bold text-gray-900">
              87%
            </p>
            <p className="mt-1 text-sm text-gray-500">
              Based on historical accuracy
            </p>
          </div>
        </div>

        <div className="card">
          <div>
            <p className="text-sm text-gray-600">Trend</p>
            <p className="mt-2 text-3xl font-bold text-green-600">
              +5.2%
            </p>
            <p className="mt-1 text-sm text-gray-500">
              Compared to last month
            </p>
          </div>
        </div>
      </div>

      {/* Top Contributing Factors */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Top Contributing Factors
        </h3>
        <div className="space-y-4">
          {[
            { factor: 'Conflict Events', impact: 0.35, trend: 'increasing' },
            { factor: 'Economic Indicators', impact: 0.28, trend: 'stable' },
            { factor: 'Climate Conditions', impact: 0.22, trend: 'worsening' },
            { factor: 'Regional Instability', impact: 0.15, trend: 'increasing' },
          ].map((item) => (
            <div key={item.factor} className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-900">
                    {item.factor}
                  </span>
                  <span className="text-sm text-gray-600">
                    {(item.impact * 100).toFixed(0)}% impact
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full"
                    style={{ width: `${item.impact * 100}%` }}
                  ></div>
                </div>
              </div>
              <span className={`ml-4 px-2 py-1 text-xs font-medium rounded-full ${
                item.trend === 'increasing'
                  ? 'bg-red-100 text-red-800'
                  : item.trend === 'stable'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-orange-100 text-orange-800'
              }`}>
                {item.trend}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
