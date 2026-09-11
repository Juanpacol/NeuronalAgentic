import { useEffect, useRef, useState } from 'react'
import type uPlot from 'uplot'
import './App.css'
import { ControlPanel } from './components/ControlPanel'
import { DietaPanel } from './components/DietaPanel'
import { FitnessChart } from './components/FitnessChart'
import { StatsBar } from './components/StatsBar'
import { ConnectionBanner } from './components/ConnectionBanner'
import { Documentacion } from './components/Documentacion'
import { TextAnimate } from './components/ui/text-animate'
import { CheshireGrin } from './components/viz/CheshireGrin'
import { useEvolutionSocket } from './hooks/useEvolutionSocket'
import { obtenerOpcionesParametros, precalentarBackend, WS_URL } from './lib/api'
import { OPCIONES_PARAMETROS_FALLBACK } from './lib/defaults'
import { generarPdfDieta } from './lib/exportarPdf'
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
  const [docAbierta, setDocAbierta] = useState(false)
  const plotRef = useRef<uPlot | null>(null)

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

  function handleDescargarPdf() {
    generarPdfDieta({
      alimentos: alimentosRef.current ?? [],
      genoma: genomaRef.current ?? [],
      objetivos: objetivosRef.current,
      canvasGrafica: plotRef.current?.ctx.canvas ?? null,
    })
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-titulo">
          <CheshireGrin tamano={56} className="cheshire-grin-inline" />
          <TextAnimate as="h1" animation="blurInUp" by="word" className="app-titulo-cheshire">
            The Cheshire Diet
          </TextAnimate>
        </div>
        <p>Laboratorio de Algoritmo Genético — un plan de alimentación que evoluciona hacia la mejor meta nutricional al menor costo</p>
      </header>

      <div className="acciones-superiores">
        <button type="button" className="boton boton-tinted ajustes-boton" onClick={() => setAjustesAbiertos(true)}>
          Ajustar metas y parámetros
        </button>
        <button type="button" className="boton boton-plain" onClick={() => setDocAbierta(true)}>
          Cómo funciona
        </button>
        <button
          type="button"
          className="boton boton-tinted"
          onClick={handleDescargarPdf}
          disabled={!stats}
        >
          Descargar informe (PDF)
        </button>
      </div>

      {docAbierta && <Documentacion onCerrar={() => setDocAbierta(false)} />}

      <ConnectionBanner status={status} mensajeError={mensajeError} onReintentar={handleIniciar} />

      <StatsBar status={status} stats={stats} inicioMs={inicioMs} maxGeneraciones={params.max_generaciones} />

      <DietaPanel alimentosRef={alimentosRef} genomaRef={genomaRef} objetivosRef={objetivosRef} />

      <FitnessChart
        historia={historia}
        activo={status === 'running'}
        onPlotListo={(plot) => {
          plotRef.current = plot
        }}
      />

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
