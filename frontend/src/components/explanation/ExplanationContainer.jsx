import React, { useState } from 'react';
import SHAPExplanation from './SHAPExplanation';
import LIMEExplanation from './LIMEExplanation';
import { Settings, Zap, Activity } from 'lucide-react';

const ExplanationContainer = ({ explanationData, explanationType = 'shap' }) => {
  const [activeTab, setActiveTab] = useState(explanationType);

  const tabs = [
    { id: 'shap', label: 'SHAP Analysis', icon: Zap, color: 'text-yellow-500' },
    { id: 'lime', label: 'LIME Explanation', icon: Activity, color: 'text-blue-500' },
    { id: 'settings', label: 'Settings', icon: Settings, color: 'text-gray-500' }
  ];

  return (
    <div className="space-y-6">
      {/* Explanation Header */}
      <div className="flex justify-between items-center pb-3 border-b">
        <h2 className="text-xl font-bold text-gray-900">
          Model Explanation
        </p>
        <div className="flex space-x-3">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-1 px-3 py-1.5 text-sm font-medium ${
                activeTab === tab.id 
                  ? 'text-primary-600 border-b-2 border-primary-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <tab.icon className={`h-4 w-4 ${tab.color}`} />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>
      
      {/* Explanation Content */}
      <div className="space-y-4">
        {activeTab === 'shap' && <SHAPExplanation explanationData={explanationData} />}
        {activeTab === 'lime' && <LIMEExplanation explanationData={explanationData} />}
        {activeTab === 'settings' && (
          <div className="text-center py-8">
            <p className="text-gray-500">Explanation settings coming soon...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExplanationContainer;
