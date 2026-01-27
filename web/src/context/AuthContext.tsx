import { 
    createContext, 
    useContext, 
    useState, 
    useEffect 
} from "react"
import type { ReactNode } from "react"
import { loginApi, getCurrentUserApi } from "../api/auth"


interface User {
    id: number
    email: string
    first_name: string | null
    last_name: string | null
    role: string
    is_active: boolean
}

interface AuthContextType {
    user: User | null
    accessToken: string | null
    isLoading: boolean
    login: (email: string, password: string) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode}) {
    const [user, setUser] = useState<User | null>(null)
    const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem('accessToken'))
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const checkAuth = async () => {
            const storedAccessToken = localStorage.getItem('accessToken')
            if (storedAccessToken) {
                try {
                    const userData = await getCurrentUserApi(storedAccessToken)
                    setUser(userData)
                    setAccessToken(storedAccessToken)
                } catch (error) {
                    localStorage.removeItem('accessToken')
                    setAccessToken(null)
                }
            }
            setIsLoading(false)
        }

        checkAuth()
    }, [])

    const login = async (email: string, password: string) => {
        const { access_token } = await loginApi(email, password)
        localStorage.setItem('accessToken', access_token)
        setAccessToken(access_token)

        const userData = await getCurrentUserApi(access_token)
        setUser(userData)
    }

    const logout = () => {
        localStorage.removeItem('accessToken')
        setAccessToken(null)
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, accessToken, isLoading, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth(){
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}