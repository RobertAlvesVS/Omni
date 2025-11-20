"use client"
import { useState, useEffect } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Lock, AlertCircle, Info, Sparkles } from "lucide-react"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  
  const { login, isAuthenticated } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, router])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError("")
    setLoading(true)
    
    try {
      await login(email, password)
    } catch (err) {
      setError("Email ou senha incorretos")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.15),rgba(255,255,255,0))]"></div>
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      
      <Card className="w-full max-w-md relative z-10 border-slate-800 bg-slate-900/90 backdrop-blur-xl shadow-2xl">
        <CardHeader className="space-y-3">
          <div className="flex justify-center mb-2">
            <div className="p-3 rounded-2xl bg-gradient-to-br from-purple-500 to-blue-500">
              <Lock className="h-8 w-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl text-center font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Login Seguro
          </CardTitle>
          <CardDescription className="text-center text-slate-400 text-base">
            Autenticação de próxima geração
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <Alert className="mb-6 border-purple-500/30 bg-purple-950/30 backdrop-blur">
            <Lock className="h-4 w-4 text-purple-400" />
            <AlertDescription className="text-purple-200 ml-2 text-sm">
              <strong className="text-purple-300">Segurança Avançada:</strong> Token em memória + Cookie HTTP-only + Criptografia end-to-end
            </AlertDescription>
          </Alert>

          <div className="space-y-5">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-slate-300 font-medium">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-purple-500 focus:ring-purple-500/20 h-12 text-base"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-slate-300 font-medium">Senha</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-purple-500 focus:ring-purple-500/20 h-12 text-base"
              />
            </div>

            {error && (
              <Alert variant="destructive" className="border-red-500/30 bg-red-950/30 backdrop-blur animate-shake">
                <AlertCircle className="h-4 w-4 text-red-400" />
                <AlertDescription className="ml-2 text-red-200">{error}</AlertDescription>
              </Alert>
            )}

            <Button 
              onClick={handleSubmit}
              className="w-full h-12 text-base font-semibold bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 transition-all duration-300 shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 hover:scale-[1.02] active:scale-[0.98]" 
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Autenticando...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" />
                  Entrar
                </span>
              )}
            </Button>
          </div>

          <Alert className="mt-6 border-slate-700 bg-slate-800/30 backdrop-blur">
            <Info className="h-4 w-4 text-slate-400" />
            <AlertDescription className="text-slate-300 ml-2 text-sm">
              <strong className="text-slate-200">Usuários de teste:</strong>
              <div className="mt-2 space-y-1 font-mono text-xs">
                <div className="text-slate-400">• user@example.com / senha123</div>
                <div className="text-slate-400">• admin@example.com / admin123</div>
              </div>
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    </div>
  )
}