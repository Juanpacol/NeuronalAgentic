import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './styles/tokens.css'
import './styles/componentes.css'
import './styles/viz.css'
import './styles/showcase.css'
import './styles/errores.css'
import App from './App.tsx'
import { ErrorBoundary } from './components/ErrorBoundary.tsx'
import { AvisoErroresGlobales } from './components/AvisoErroresGlobales.tsx'
import { Showcase } from './components/ui/Showcase.tsx'
import { registrarListenersGlobales } from './lib/errores'

// Los errores asíncronos (setTimeout, promesas, onmessage del WebSocket) no los
// atrapa ningún ErrorBoundary; se capturan aquí y se muestran como aviso flotante.
registrarListenersGlobales()

// Vista de muestra del sistema de diseño, sin backend: abrir con ?showcase=1
const mostrarShowcase = new URLSearchParams(window.location.search).has('showcase')

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <AvisoErroresGlobales />
      {mostrarShowcase ? <Showcase /> : <App />}
    </ErrorBoundary>
  </StrictMode>,
)
