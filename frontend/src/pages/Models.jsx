import { useState } from 'react'
import { Brain, TrendingUp, CheckCircle, XCircle } from 'lucide-react'

export default function Models() {
  const [models] = useState([
    {
      id: 1,
      name: 'LSTM Displacement Forecaster',
      type: 'LSTM',
      version: 'v1.2.0',
      status: 'active',
      accuracy: 0.87,
      rmse: 125.4,
      trainedOn: '2024-01-10',
      features: 45,
    },
    {
      id: 2,
      name: 'XGBoost Multi-Factor Model',
      type: 'XGBoost',
      version: 'v2.0.1',
      status: 'active',
      accuracy: 0.91,
      rmse: 98.2,
      trainedOn: '2024-01-12',
      features: 52,
    },
    {
      id: 3,
      name: 'Random Forest Baseline',
      type: 'RandomForest',
      version: 'v1.0.0',
      status: 'inactive',
      accuracy: 0.82,
      rmse: 156.8,
      trainedOn: '2024-01-05',
      features: 38,
    },
  ])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">ML Models</h2>
          <p className="mt-2 text-gray-600">
            Manage and monitor machine learning models
          </p>
        </div>
        
        <button className="btn btn-primary">
          Train New Model
        </button>
      </div>

      {/* Models Grid */}
      <div className="grid grid-cols-1 gap-6">
        {models.map((model) => (
          <div key={model.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <Brain className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <div className="flex items-center space-x-3">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {model.name}
                    </h3>
                    {model.status === 'active' ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : (
                      <XCircle className="w-5 h-5 text-gray-400" />
                    )}
                  </div>
                  <p className="mt-1 text-sm text-gray-600">
                    {model.type} • {model.version} • {model.features} features
                  </p>
                </div>
              </div>
              
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                model.status === 'active'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {model.status}
              </span>
            </div>

            <div className="mt-6 grid grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600">Accuracy (R²)</p>
                <p className="mt-1 text-2xl font-bold text-gray-900">
                  {(model.accuracy * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">RMSE</p>
                <p className="mt-1 text-2xl font-bold text-gray-900">
                  {model.rmse}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Trained On</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {model.trainedOn}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Features</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {model.features} variables
                </p>
              </div>
            </div>

            <div className="mt-6 flex space-x-2">
              <button className="btn btn-secondary">
                View Details
              </button>
              <button className="btn btn-secondary">
                Explainability
              </button>
              {model.status === 'inactive' && (
                <button className="btn btn-primary">
                  Activate
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Model Comparison */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Model Performance Comparison
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  R² Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  RMSE
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  MAE
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {models.map((model) => (
                <tr key={model.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {model.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {model.type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {model.accuracy.toFixed(3)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {model.rmse}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {(model.rmse * 0.8).toFixed(1)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
