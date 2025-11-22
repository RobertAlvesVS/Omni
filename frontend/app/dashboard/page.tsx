// app/dashboard/page.tsx
"use client"

import { useEffect } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { Separator } from "@/components/ui/separator"

export default function DashboardPage() {
  const { user, logout, isAuthenticated, isLoading, accessToken } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      console.log("⚠️ Não autenticado, redirecionando...")
      router.push("/login")
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        Carregando...
      </div>
    )
  }

  if (!isAuthenticated) return null

  return (
    <div className="container mx-auto p-6 min-h-screen">
      <Card className="shadow-md border">
        <CardHeader>
          <CardTitle className="text-2xl">Dashboard</CardTitle>
        </CardHeader>

        <CardContent className="space-y-6">

          {/* Segurança */}
          <Alert className="border-blue-500 bg-blue-50">
            <AlertTitle className="text-blue-700 font-semibold">🔒 Segurança Implementada</AlertTitle>
            <AlertDescription>
              <ul className="list-disc ml-4 space-y-1">
                <li>Access Token apenas em memória (state)</li>
                <li>Refresh Token via cookie HTTP-only</li>
                <li>Proteção contra XSS e CSRF</li>
                <li>Renovação automática do token ao recarregar</li>
              </ul>
            </AlertDescription>
          </Alert>

          <Separator />

          {/* Dados do Usuário */}
          <Card className="bg-muted/50">
            <CardHeader>
              <CardTitle className="text-lg">👤 Dados do Usuário</CardTitle>
              <CardDescription>Informações da sessão autenticada</CardDescription>
            </CardHeader>
            <CardContent className="space-y-1 text-sm">
              <p><strong>ID:</strong> {user?.id}</p>
              <p><strong>Nome:</strong> {user?.nome}</p>
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Criado em:</strong> {new Date(user?.criado_em || "").toLocaleString("pt-BR")}</p>
            </CardContent>
          </Card>

          {/* Token debug */}
          <Alert className="bg-yellow-50 border-yellow-500">
            <AlertTitle className="font-medium">🔑 Token (Debug)</AlertTitle>
            <AlertDescription className="space-y-2 text-sm">
              <p><strong>Access Token:</strong></p>
              <code className="block p-2 bg-white rounded text-xs overflow-x-auto">
                {accessToken ? `${accessToken.substring(0, 50)}...` : "Nenhum"}
              </code>
              <p className="text-xs text-muted-foreground">
                ℹ️ Refresh Token não é exibido (HTTP-only)
              </p>
            </AlertDescription>
          </Alert>

          {/* Botões */}
          <div className="flex gap-4">
            <Button 
              variant="default"
              onClick={() => {
                alert("Recarregue a página (F5) para testar o refresh automatico.")
              }}
            >
              🧪 Testar Refresh Token
            </Button>

            <Button variant="destructive" onClick={logout}>
              🚪 Sair
            </Button>
          </div>

          {/* Instruções */}
          <Card className="bg-slate-50">
            <CardHeader>
              <CardTitle className="text-sm font-medium">💡 Como testar</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="list-decimal ml-4 text-sm space-y-1">
                <li>Clique em Testar Refresh Token</li>
                <li>Recarregue a página e continue logado</li>
                <li>Feche e abra o navegador: ainda logado</li>
                <li>Logout apenas ao clicar ou após expiração</li>
              </ol>
            </CardContent>
          </Card>

        </CardContent>
      </Card>
    </div>
  )
}
