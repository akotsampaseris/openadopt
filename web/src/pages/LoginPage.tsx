import { useForm } from "react-hook-form"
import { useAuth } from "../context/AuthContext"
import { useState, useEffect } from "react"
import { useNavigate } from 'react-router-dom'

interface LoginFormData {
    email: string
    password: string
}

export default function LoginPage() {
    const { 
        register, handleSubmit, formState: { errors, isSubmitting } 
    } = useForm<LoginFormData>()
    const { login, accessToken } = useAuth()
    const navigate = useNavigate()
    const [error, setError] = useState<string>('')

    const onSubmit = async (data: LoginFormData) => {
        try {
            setError('')
            await login(data.email, data.password)
            navigate('/admin/dashboard')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Login failed')
        }
    }

    useEffect(() => {
        if (accessToken) {
            console.log(accessToken)
            navigate('/admin/dashboard')
        }
    }, [accessToken, navigate])

    return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">OpenAdopt Admin</h1>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Email</label>
            <input
              type="email"
              {...register('email', { required: 'Email is required' })}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            />
            {errors.email && (
              <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium">Password</label>
            <input
              type="password"
              {...register('password', { required: 'Password is required' })}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
            />
            {errors.password && (
              <p className="text-red-600 text-sm mt-1">{errors.password.message}</p>
            )}
          </div>

          {error && (
            <div className="bg-red-200 text-red-600 p-3 rounded-md text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  )
}