import { useEffect, useState } from 'react'
import './App.css'
import { ControlPanel } from './components/ControlPanel'
import { RouteCanvas } from './components/RouteCanvas'
import { exportarRutaComoPng } from './lib/canvas'
import { FitnessChart } from './components/FitnessChart'
import { StatsBar } from './components/StatsBar'
import { ConnectionBanner } from './components/ConnectionBanner'
import { useEvolutionSocket } from './hooks/useEvolutionSocket'
import { obtenerOpcionesParametros, precalentarBackend, WS_URL } from './lib/api'
import { OPCIONES_PARAMETROS_FALLBACK } from './lib/defaults'
import type { OpcionesParametros, ParametrosAG } from './lib/tipos'

/**
 * App.tsx es el dueño único del estado de `params` (useState, sin Redux/Zustand/Context:
 * innecesario a esta escala). Orquesta el hook de WebSocket y organiza el layout.
 */
function App() {
  const [opciones, setOpciones] = useState<OpcionesParametros>(OPCIONES_PARAMETROS_FALLBACK)
  const [params, setParams] = useState<ParametrosAG>(OPCIONES_PARAMETROS_FALLBACK.defaults)
  const [inicioMs, setInicioMs] = useState<number | null>(null)

  const { status, stats, historia, ciudadesRef, rutaRef, iniciar, pausar, reanudar, detener, mensajeError } =
    useEvolutionSocket(WS_URL)

  // Al montar: precalienta el backend (puede estar dormido en Render) y carga opciones.
  useEffect(() => {
    precalentarBackend()

    obtenerOpcionesParametros().then((op) => {
      setOpciones(op)
      setParams(op.defaults)
    })
  }, [])

  function handleIniciar() {
    setInicioMs(Date.now())
    iniciar(params)
  }

  function handleDetener() {
    detener()
    setInicioMs(null)
  }

  function handleExportar() {
    exportarRutaComoPng(ciudadesRef.current, rutaRef.current, `ruta-generacion-${stats?.generacion ?? 0}.png`)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Laboratorio de Algoritmo Genético — TSP</h1>
        <p>Evolución de una ruta hacia el recorrido más corto</p>
      </header>

      <ConnectionBanner status={status} mensajeError={mensajeError} onReintentar={handleIniciar} />

      <StatsBar status={status} stats={stats} inicioMs={inicioMs} />

      <div className="canvases-row">
        <div className="canvas-column">
          <h2>Ruta</h2>
          <RouteCanvas ciudadesRef={ciudadesRef} rutaRef={rutaRef} />
          <button type="button" onClick={handleExportar}>
            Exportar PNG
          </button>
        </div>
      </div>

      <FitnessChart historia={historia} />

      <ControlPanel
        params={params}
        onChange={setParams}
        opciones={opciones.opciones}
        status={status}
        onIniciar={handleIniciar}
        onPausar={pausar}
        onReanudar={reanudar}
        onDetener={handleDetener}
      />
    </div>
  )
}

export default App
