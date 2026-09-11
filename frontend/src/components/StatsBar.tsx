import { useEffect, useState } from 'react'
import type { EstadisticasActuales, EstadoConexion } from '../lib/tipos'

interface StatsBarProps {
  status: EstadoConexion
  stats: EstadisticasActuales | null
  inicioMs: number | null
}

const ETIQUETAS_ESTADO: Record<EstadoConexion, string> = {
  idle: 'Inactivo',
  connecting: 'Conectando…',
  waking: 'Despertando servidor…',
  open: 'Conectado',
  running: 'Ejecutando',
  paused: 'Pausado',
  reconnecting: 'Reconectando…',
  error: 'Error',
}

function formatearTiempo(ms: number): string {
  const totalSeg = Math.floor(ms / 1000)
  const min = Math.floor(totalSeg / 60)
  const seg = totalSeg % 60
  return `${min}:${seg.toString().padStart(2, '0')}`
}

/** Contador de generación, tiempo transcurrido, aptitud y penalizaciones de la mejor dieta. */
export function StatsBar({ status, stats, inicioMs }: StatsBarProps) {
  const [ahora, setAhora] = useState(() => Date.now())

  useEffect(() => {
    if (status !== 'running' && status !== 'paused') return
    const id = setInterval(() => setAhora(Date.now()), 1000)
    return () => clearInterval(id)
  }, [status])

  const transcurridoMs = inicioMs ? ahora - inicioMs : 0

  return (
    <div className="stats-bar">
      <span className={`badge badge-${status}`}>{ETIQUETAS_ESTADO[status]}</span>
      <span>Generación: {stats?.generacion ?? '—'}</span>
      <span>Tiempo: {formatearTiempo(transcurridoMs)}</span>
      <span>Mejor aptitud: {stats ? stats.mejor_aptitud.toFixed(4) : '—'}</span>
      <span>Aptitud promedio: {stats ? stats.aptitud_promedio.toFixed(4) : '—'}</span>
      <span>Desviación de macros: {stats ? stats.pen_macro.toFixed(3) : '—'}</span>
      <span>Desviación de costo: {stats ? stats.pen_costo.toFixed(3) : '—'}</span>
      <span>Sin mejora: {stats?.generaciones_sin_mejora ?? '—'}</span>
    </div>
  )
}
