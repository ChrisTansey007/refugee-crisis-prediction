import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import MapView from './pages/MapView'
import DataSources from './pages/DataSources'
import Models from './pages/Models'
import Predictions from './pages/Predictions'
import Reports from './pages/Reports'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/map" element={<MapView />} />
        <Route path="/data-sources" element={<DataSources />} />
        <Route path="/models" element={<Models />} />
        <Route path="/predictions" element={<Predictions />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Layout>
  )
}

export default App
