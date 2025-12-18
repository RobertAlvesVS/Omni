// contexts/AuthContext.tsx
"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'

// Adapte este tipo conforme seu modelo Usuario
interface User {
  id: number
  nome: string
  email: string
  criado_em: string
}

interface AuthContextType {
  user: User | null
  accessToken: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
  isAuthenticated: boolean
  refreshAccessToken: () => Promise<string | null>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [accessToken, setAccessToken] = useState<string | null>(null) // EM MEMÓRIA!
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  // Tenta restaurar a sessão ao montar o componente
  useEffect(() => {
    const initAuth = async () => {
      const token = await refreshAccessToken()
      if (token) {
        await fetchUserData(token)
      }
      setIsLoading(false)
    }
    initAuth()
  }, [])

  // Busca dados do usuário
  async function fetchUserData(token: string) {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include' // Importante para cookies
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        setAccessToken(token)
      } else {
        setAccessToken(null)
        setUser(null)
      }
    } catch (error) {
      setAccessToken(null)
      setUser(null)
    }
  }

  // Renova o access token usando o refresh token do cookie
  async function refreshAccessToken(): Promise<string | null> {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh_token`, {
        method: 'POST',
        credentials: 'include', // Envia o cookie com refresh_token
      })

      if (response.ok) {
        const data = await response.json()
        setAccessToken(data.access_token)
        return data.access_token
      }
      return null
    } catch {
      return null
    }
  }

  // Login
  async function login(email: string, password: string) {
    // FastAPI OAuth2 espera form-urlencoded com 'username' (não 'email')
    const formData = new URLSearchParams()
    formData.append('username', email)  // OAuth2 usa 'username'
    formData.append('password', password)

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      credentials: 'include', // IMPORTANTE: para receber o cookie
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Credenciais inválidas')
    }

    const data = await response.json()

    // Access token fica APENAS em memória (não em localStorage!)
    setAccessToken(data.access_token)

    // Busca dados do usuário
    await fetchUserData(data.access_token)

    // Redireciona para dashboard
    router.push('/dashboard')
  }

  // Logout
  async function logout() {
    try {
      // Chama endpoint de logout no backend para limpar cookie
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      })
    }catch{
      router.push('/login')
      setAccessToken(null)
      setUser(null)
    }

    setAccessToken(null)
    setUser(null)
    router.push('/login')
  }

  return (
    <AuthContext.Provider value={{
      user,
      accessToken,
      login,
      logout,
      isLoading,
      isAuthenticated: !!user,
      refreshAccessToken
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider')
  }
  return context
}