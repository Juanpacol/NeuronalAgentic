import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './styles/errores.css'
import App from './App.tsx'
import { ErrorBoundary } from './components/ErrorBoundary.tsx'
import { AvisoErroresGlobales } from './components/AvisoErroresGlobales.tsx'
import { registrarListenersGlobales } from './lib/errores'

// Los errores asíncronos (setTimeout, promesas, onmessage del WebSocket) no los
// atrapa ningún ErrorBoundary; se capturan aquí y se muestran como aviso flotante.
registrarListenersGlobales()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <AvisoErroresGlobales />
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
