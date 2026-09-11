import { useEffect, useState } from 'react'
import './App.css'
import { ControlPanel } from './components/ControlPanel'
import { GenomeCanvas } from './components/GenomeCanvas'
import { exportarGenomaComoPng } from './lib/canvas'
import { TargetPanel } from './components/TargetPanel'
import { FitnessChart } from './components/FitnessChart'
import { StatsBar } from './components/StatsBar'
import { ConnectionBanner } from './components/ConnectionBanner'
import { useEvolutionSocket } from './hooks/useEvolutionSocket'
import { obtenerOpcionesParametros, obtenerTargets, precalentarBackend, WS_URL } from './lib/api'
import { OPCIONES_PARAMETROS_FALLBACK } from './lib/defaults'
import type { OpcionesParametros, ParametrosAG, TargetInfo } from './lib/tipos'

/**
 * App.tsx es el dueño único del estado de `params` (useState, sin Redux/Zustand/Context:
 * innecesario a esta escala). Orquesta el hook de WebSocket y organiza el layout.
 */
function App() {
  const [opciones, setOpciones] = useState<OpcionesParametros>(OPCIONES_PARAMETROS_FALLBACK)
  const [params, setParams] = useState<ParametrosAG>(OPCIONES_PARAMETROS_FALLBACK.defaults)
  const [targets, setTargets] = useState<TargetInfo[]>([])
  const [targetId, setTargetId] = useState<string>('default')
  const [inicioMs, setInicioMs] = useState<number | null>(null)

  const { status, stats, historia, genomaRef, iniciar, pausar, reanudar, detener, mensajeError } =
    useEvolutionSocket(WS_URL)

  // Al montar: precalienta el backend (puede estar dormido en Render) y carga opciones/targets.
  useEffect(() => {
    precalentarBackend()

    obtenerOpcionesParametros().then((op) => {
      setOpciones(op)
      setParams(op.defaults)
    })

    obtenerTargets().then((lista) => {
      setTargets(lista)
      if (lista.length > 0) {
        setTargetId(lista[0].id)
      }
    })
  }, [])

  function handleIniciar() {
    setInicioMs(Date.now())
    iniciar(params, targetId)
  }

  function handleDetener() {
    detener()
    setInicioMs(null)
  }

  function handleExportar() {
    exportarGenomaComoPng(genomaRef.current, `genoma-generacion-${stats?.generacion ?? 0}.png`)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Laboratorio de Algoritmo Genético</h1>
        <p>Evolución de triángulos hacia una imagen objetivo</p>
      </header>

      <ConnectionBanner status={status} mensajeError={mensajeError} onReintentar={handleIniciar} />

      <StatsBar status={status} stats={stats} inicioMs={inicioMs} />

      <div className="canvases-row">
        <div className="canvas-column">
          <h2>Evolución</h2>
          <GenomeCanvas genomaRef={genomaRef} />
          <button type="button" onClick={handleExportar}>
            Exportar PNG
          </button>
        </div>
        <div className="canvas-column">
          <h2>Objetivo</h2>
          <TargetPanel />
        </div>
      </div>

      <FitnessChart historia={historia} />

      <ControlPanel
        params={params}
        onChange={setParams}
        opciones={opciones.opciones}
        status={status}
        targets={targets}
        targetId={targetId}
        onTargetIdChange={setTargetId}
        onIniciar={handleIniciar}
        onPausar={pausar}
        onReanudar={reanudar}
        onDetener={handleDetener}
      />
    </div>
  )
}

export default App
