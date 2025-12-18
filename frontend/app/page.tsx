"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/AuthContext"
import { Loader2 } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

export default function HomePage() {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        router.push('/dashboard')
      } else {
        router.push('/login')
      }
    }
  }, [isAuthenticated, isLoading, router])

  return (
    <div className="flex min-h-screen items-center justify-center bg-linear-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      <Card className="w-full max-w-md border-slate-200 dark:border-slate-800">
        <CardContent className="flex flex-col items-center justify-center gap-4 p-8">
          <Loader2 className="h-12 w-12 animate-spin text-primary" />
          <div className="text-center space-y-2">
            <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
              Verificando autenticação
            </h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Aguarde um momento...
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}