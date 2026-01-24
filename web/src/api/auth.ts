import { apiClient } from "./client";

interface LoginRequest {
    email: string
    password: string
}

interface TokenResponse {
    access_token: string
    token_type: string
}

interface UserResponse {
    id: number
    email: string
    first_name: string | null
    last_name: string | null
    role: string
    is_active: boolean
}

export async function loginApi(
    email: string, 
    password: string
): Promise<TokenResponse>{
    const { data } = await apiClient.post<TokenResponse>('/auth/login', {
        email,
        password
    })
    return data
}

export async function getCurrentUserApi(access_token: string): Promise<UserResponse>{
    const { data } = await apiClient.get<UserResponse>('/auth/me', {
        headers: {
            Authorization: `Bearer ${access_token}`
        }
    })
    return data
}