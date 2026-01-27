import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { useAuth } from "./context/AuthContext"
import LoginPage from "./pages/LoginPage"
import AdminDashboardPage from "./pages/admin/AdminDashboard"

import AnimalsPage from "./pages/admin/AnimalsPage"
import AnimalFormPage from "./pages/admin/AnimalFormPage"
import AnimalDetailsPage from "./pages/admin/AnimalDetailsPage"

function App() {
  const { isLoading } = useAuth()

  if(isLoading){
    return <div>Loading...</div>
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to='/admin/dashboard' />} />
        <Route path="/admin/login" element={<LoginPage />} />
        <Route path="/admin/dashboard" 
          element={<ProtectedRoute><AdminDashboardPage /></ProtectedRoute>} />
        <Route path="/admin/animals" 
          element={<ProtectedRoute><AnimalsPage /></ProtectedRoute>} />
        <Route path="/admin/animals/:id" element={
          <ProtectedRoute><AnimalDetailsPage /></ProtectedRoute>} />
        <Route path="/admin/animals/new" 
          element={<ProtectedRoute><AnimalFormPage /></ProtectedRoute>} />
        <Route path="/admin/animals/:id/edit" 
          element={<ProtectedRoute><AnimalFormPage /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { accessToken, isLoading } = useAuth()
  
  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }
  
  return accessToken ? <>{children}</> : <Navigate to="/admin/login" />
}

export default App
