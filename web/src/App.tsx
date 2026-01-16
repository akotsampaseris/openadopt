import './App.css'

import { useHealthCheck } from './hooks/useHealthCheck'

function App() {
  const { data, isLoading, error } = useHealthCheck();

  return (
    <>
      <div className="bg-gray-400 p-4 rounded">
        {isLoading && <p>Checking API...</p>}
        {error && <p className="text-red-900">API Error</p>}
        {data && (
          <p className="text-green-900">API Status: {data.status}</p>
        )}
      </div>
    </>
  )
}

export default App
