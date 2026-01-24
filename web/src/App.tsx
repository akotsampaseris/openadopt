import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { useAuth } from "./context/AuthContext"
import LoginPage from "./pages/LoginPage"

function App() {
  const { isLoading } = useAuth()

  if(isLoading){
    return <div>Loading...</div>
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/admin/login" element={<LoginPage />} />
        <Route path="/" element={<Navigate to="/admin/login" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
