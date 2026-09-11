import { useEffect, useState } from 'react'
import './App.css'
import { ControlPanel } from './components/ControlPanel'
import { DietaPanel } from './components/DietaPanel'
import { FitnessChart } from './components/FitnessChart'
import { StatsBar } from './components/StatsBar'
import { ConnectionBanner } from './components/ConnectionBanner'
import { TextAnimate } from './components/ui/text-animate'
import { useEvolutionSocket } from './hooks/useEvolutionSocket'
import { obtenerOpcionesParametros, precalentarBackend, WS_URL } from './lib/api'
import { OPCIONES_PARAMETROS_FALLBACK } from './lib/defaults'
import type { OpcionesParametros, ParametrosAG } from './lib/tipos'

/**
 * App.tsx es el dueño único del estado de `params` (useState, sin Redux/Zustand/Context:
 * innecesario a esta escala). Orquesta el hook de WebSocket y organiza el layout.
 *
 * Los ajustes (ControlPanel) viven en un sidebar aparte de los resultados
 * (StatsBar/DietaPanel/FitnessChart): antes de calcular, el usuario solo ve
 * ajustes; al presionar Iniciar el sidebar se cierra solo y deja ver los
 * resultados, sin las dos secciones compitiendo por espacio a la vez.
 */
function App() {
  const [opciones, setOpciones] = useState<OpcionesParametros>(OPCIONES_PARAMETROS_FALLBACK)
  const [params, setParams] = useState<ParametrosAG>(OPCIONES_PARAMETROS_FALLBACK.defaults)
  const [inicioMs, setInicioMs] = useState<number | null>(null)
  const [ajustesAbiertos, setAjustesAbiertos] = useState(true)

  const {
    status,
    stats,
    historia,
    alimentosRef,
    genomaRef,
    objetivosRef,
    iniciar,
    pausar,
    reanudar,
    detener,
    mensajeError,
  } = useEvolutionSocket(WS_URL)

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
    setAjustesAbiertos(false)
  }

  function handleDetener() {
    detener()
    setInicioMs(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <TextAnimate as="h1" animation="blurInUp" by="word">
          Laboratorio de Algoritmo Genético — Dieta
        </TextAnimate>
        <p>Evolución de un plan de alimentación hacia la mejor meta nutricional al menor costo</p>
      </header>

      <button type="button" className="boton boton-tinted ajustes-boton" onClick={() => setAjustesAbiertos(true)}>
        Ajustar metas y parámetros
      </button>

      <ConnectionBanner status={status} mensajeError={mensajeError} onReintentar={handleIniciar} />

      <StatsBar status={status} stats={stats} inicioMs={inicioMs} maxGeneraciones={params.max_generaciones} />

      <DietaPanel alimentosRef={alimentosRef} genomaRef={genomaRef} objetivosRef={objetivosRef} />

      <FitnessChart historia={historia} />

      {ajustesAbiertos && (
        <div className="sidebar-backdrop" onClick={() => setAjustesAbiertos(false)} />
      )}
      <aside className={`sidebar${ajustesAbiertos ? ' sidebar-abierto' : ''}`} aria-hidden={!ajustesAbiertos}>
        <div className="sidebar-cabecera">
          <h2>Ajustes de la dieta</h2>
          <button
            type="button"
            className="sidebar-cerrar"
            onClick={() => setAjustesAbiertos(false)}
            aria-label="Cerrar ajustes"
          >
            ✕
          </button>
        </div>
        <div className="sidebar-cuerpo">
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
      </aside>
    </div>
  )
}

export default App
