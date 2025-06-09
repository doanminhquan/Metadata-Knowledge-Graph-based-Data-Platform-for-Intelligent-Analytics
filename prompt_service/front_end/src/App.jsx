import './App.css'
import { Routes, Route } from 'react-router-dom'
import PromptToDashboard from './pages/Prompt.jsx'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<PromptToDashboard />} />
        {/* <Route path="/history" element={<Placeholder title="Lịch sử" />} />
        <Route path="/profile" element={<Placeholder title="Hồ sơ cá nhân" />} />
        <Route path="/dashboards" element={<Placeholder title="Bảng điều khiển của tôi" />} /> */}
      </Routes>
    </div>
  )
}

export default App