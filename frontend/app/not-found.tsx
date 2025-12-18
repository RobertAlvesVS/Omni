import Link from 'next/link'
import { Home, AlertTriangle } from 'lucide-react' // Removi Search, MapPin, Compass
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-950 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-4 rounded-full bg-red-100 dark:bg-red-950">
              <AlertTriangle className="h-12 w-12 text-red-600 dark:text-red-400" />
            </div>
          </div>
          <CardTitle className="text-3xl">404 - Página não encontrada</CardTitle>
          <CardDescription>
            A página que você está procurando não existe ou foi movida.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Button asChild className="w-full">
            <Link href="/">
              <Home className="mr-2 h-4 w-4" />
              Voltar para Home
            </Link>
          </Button>
          <p className="text-sm text-center text-muted-foreground">
            Se você acha que isso é um erro, entre em contato com o suporte.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}