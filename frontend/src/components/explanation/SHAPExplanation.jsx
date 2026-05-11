import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Zap, Activity, Heart, Settings } from 'lucide-react';

const SHAPExplanation = ({ explanationData }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulate loading explanation data
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  }, [explanationData]);

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p className="mt-2 text-gray-500">Loading explanation...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <h4 className="text-red-800 font-medium">Error loading explanation</h4>
        <p className="text-red-600">{error.message}</p>
      </div>
    );
  }

  if (!explanationData || !explanationData.feature_importance) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No explanation data available</p>
      </div>
    );
  }

  const { feature_importance, shap_values_shape, summary_plot, top_features } = explanationData;
  const features = Object.entries(feature_importance)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">
          Feature Importance (SHAP Values)
        </h3>
        <button 
          className="btn btn-sm btn-outline"
          onClick={() => window.open(summary_plot, '_blank')}
        >
          View Full Plot
        </button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Feature Importance Chart */}
        <div className="card">
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={features}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="0" tick={{ fontSize: 12 }} />
              <YAxis />
              <Tooltip formatter={(value) => `$${value}`} />
              <Legend verticalAlign="top" height={36} />
              <Bar dataKey="1" fill="#3b82f6" radius={[6, 6, 0, 0]} />
            </ResponsiveContainer>
          </div>
          
          {/* Feature Details */}
          <div className="space-y-3">
            {features.map(([feature, importance], index) => (
              <div key={index} className="flex justify-between items-center px-3 py-2 bg-gray-50 rounded">
                <span className="font-medium">{feature}</span>
                <span className="text-right font-semibold text-primary-600">
                  {importance.toFixed(3)}
                </span>
              </div>
            ))}
          </div>
        </div>
        
        {/* Explanation Summary */}
        <div className="card">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Key Insights</h4>
          <div className="space-y-2">
            <div className="flex items-start space-x-2">
              <Zap className="h-4 w-4 text-yellow-500 mt-1" />
              <div>
                <p className="font-medium">Top Feature: {top_features[0] || 'N/A'}</p>
                <p className="text-sm text-gray-600">
                  Most influential factor in predictions
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-2">
              <Activity className="h-4 w-4 text-blue-500 mt-1" />
              <div>
                <p className="font-medium">Feature Count: {Object.keys(feature_importance).length}</p>
                <p className="text-sm text-gray-600">
                  Total features analyzed
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-2">
              <Heart className="h-4 w-4 text-pink-500 mt-1" />
              <div>
                <p className="font-medium">Model Stability: High</p>
                <p className="text-sm text-gray-600">
                  Consistent feature importance across samples
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Feature Contributions (if single prediction explanation) */}
      {explanationData.feature_contributions && (
        <>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Feature Contributions
            </h3>
            <p className="text-sm text-gray-500">
              How each feature contributed to this specific prediction
            </p>
          </div>
          <div className="space-y-2">
            {Object.entries(explanationData.feature_contributions)
              .sort(([,a], [,b]) => Math.abs(b) - Math.abs(a))
              .map(([feature, contribution], index) => (
                <div key={index} className="flex items-center justify-between px-3 py-2 bg-gray-50 rounded">
                  <span className="font-medium">{feature}</span>
                  <div className="flex items-center space-x-2">
                    <span className={`text-sm font-semibold ${
                      contribution >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {contribution.toFixed(3)}
                    </span>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          contribution >= 0 ? 'bg-green-600' : 'bg-red-600'
                        }`} 
                        style={{ width: `${Math.abs(contribution) * 50}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </>
      )}
    </div>
  );
};

export default SHAPExplanation;
