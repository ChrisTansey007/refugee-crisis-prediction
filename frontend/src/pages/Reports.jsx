import { FileText, Download } from 'lucide-react'

export default function Reports() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Reports</h2>
          <p className="mt-2 text-gray-600">
            Generate and export analysis reports
          </p>
        </div>
        
        <button className="btn btn-primary">
          Create New Report
        </button>
      </div>

      {/* Report Templates */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          {
            name: 'Monthly Summary',
            description: 'Comprehensive monthly displacement analysis',
            icon: FileText,
          },
          {
            name: 'Country Profile',
            description: 'Detailed country-specific report',
            icon: FileText,
          },
          {
            name: 'Trend Analysis',
            description: 'Historical trends and forecasts',
            icon: FileText,
          },
        ].map((template) => {
          const Icon = template.icon
          return (
            <div key={template.name} className="card">
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-primary-100 rounded-lg">
                  <Icon className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {template.name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    {template.description}
                  </p>
                </div>
              </div>
              <button className="mt-4 btn btn-secondary w-full">
                Generate
              </button>
            </div>
          )
        })}
      </div>

      {/* Recent Reports */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Reports
        </h3>
        <div className="space-y-3">
          {[
            { name: 'Afghanistan Monthly Report - January 2024', date: '2024-01-15', size: '2.4 MB' },
            { name: 'Syria Trend Analysis Q4 2023', date: '2024-01-10', size: '3.1 MB' },
            { name: 'Regional Overview - East Africa', date: '2024-01-08', size: '4.8 MB' },
          ].map((report) => (
            <div
              key={report.name}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">{report.name}</p>
                  <p className="text-xs text-gray-500">{report.date} • {report.size}</p>
                </div>
              </div>
              <button className="p-2 hover:bg-gray-200 rounded-lg transition-colors">
                <Download className="w-5 h-5 text-gray-600" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
