import { useAuth } from '@/contexts/AuthContext'

export class APIClient {
  private baseURL: string
  private getAccessToken: () => string | null
  private refreshAccessToken: () => Promise<string | null>

  constructor(
    getAccessToken: () => string | null,
    refreshAccessToken: () => Promise<string | null>
  ) {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    this.getAccessToken = getAccessToken
    this.refreshAccessToken = refreshAccessToken
  }

  async fetch(endpoint: string, options: RequestInit = {}): Promise<Response> {
    let token = this.getAccessToken()

    const makeRequest = async (accessToken: string | null) => {
      const headers: HeadersInit = {
        ...options.headers,
      }

      if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`
      }

      return fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        credentials: 'include', // Sempre inclui cookies
        headers
      })
    }

    let response = await makeRequest(token)

    // Se 401, tenta renovar o token
    if (response.status === 401) {
      const newToken = await this.refreshAccessToken()
      if (newToken) {
        response = await makeRequest(newToken)
      }
    }

    return response
  }
}

// Hook para usar o API Client
export function useAPIClient() {
  const { accessToken, refreshAccessToken } = useAuth()
  
  return new APIClient(
    () => accessToken,
    refreshAccessToken
  )
}