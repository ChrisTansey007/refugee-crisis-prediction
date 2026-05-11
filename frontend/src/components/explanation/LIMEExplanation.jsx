import React from 'react';
import { Pie, PieChart, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Zap, Activity, Heart, Settings } from 'lucide-react';

const LIMEExplanation = ({ explanationData }) => {
  if (!explanationData || !explanationData.feature_contributions) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No LIME explanation data available</p>
      </div>
    );
  }

  const { feature_contributions, prediction, base_value } = explanationData;
  const contributions = Object.entries(feature_contributions)
    .filter(([,value]) => Math.abs(value) > 0.001) // Filter near-zero contributions
    .sort(([,a], [,b]) => Math.abs(b) - Math.abs(a));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-900">
          Feature Contributions (LIME)
        </h3>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Contribution Pie Chart */}
        <div className="card">
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie 
                data={contributions.map(([feature, value]) => ({
                  name: feature,
                  value: Math.abs(value),
                  contribution: value
                }))}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius="60%"
                outerRadius="80%"
                labelLine={false}
                label={({ name, value, contribution }) => (
                  <div className="text-[10px]">
                    {name}: {contribution >= 0 ? '+' : ''}{contribution.toFixed(2)}
                  </div>
                )}
              >
                {contributions.map((_, index) => (
                  <Cell key={index} fill={`hsl(${index * 30}, 70%, 50%)`} />
                ))}
              </Pie>
            </ResponsiveContainer>
          </div>
          
          {/* Prediction Details */}
          <div className="card">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Prediction Breakdown</h4>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Base Value</span>
                <span className="font-mono text-gray-900">{base_value.toFixed(1)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Feature Contributions</span>
                <span className="font-mono text-gray-900">
                  {contributions.reduce((sum, [,value]) => sum + value, 0).toFixed(1)}
                </span>
              </div>
              <div className="flex justify-between items-center pt-2 border-t">
                <span className="text-gray-600 font-medium">Final Prediction</span>
                <span className="text-2xl font-bold text-primary-600">
                  {prediction.toFixed(1)}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Feature Details List */}
        <div className="card">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Feature Details</h4>
          <div className="space-y-2">
            {contributions.map(([feature, contribution], index) => (
              <div key={index} className="flex justify-between items-center px-3 py-2 bg-gray-50 rounded">
                <span className="font-medium">{feature}</span>
                <div className="flex items-center space-x-2">
                  <span className={`text-sm font-semibold ${
                    contribution >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {contribution.toFixed(3)}
                  </span>
                  {contribution >= 0 ? (
                    <TrendingUp className="h-4 w-4 text-green-500" />
                  ) : (
                    <TrendingDown className="h-4 w-4 text-red-500" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LIMEExplanation;
