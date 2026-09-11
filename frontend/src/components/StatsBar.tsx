import { useEffect, useRef, useState } from 'react'
import type { EstadisticasActuales, EstadoConexion } from '../lib/tipos'
import { StatTile } from './ui/StatTile'
import { GenerationCounter } from './viz/GenerationCounter'
import { NumberTicker } from './ui/number-ticker'

interface StatsBarProps {
  status: EstadoConexion
  stats: EstadisticasActuales | null
  inicioMs: number | null
  maxGeneraciones: number
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

/**
 * Menú de métricas compacto: una sola fila que envuelve (grid auto-fit), sin
 * scroll. El anillo de generación y los StatTile se refrescan al mismo ritmo
 * ~8Hz que el resto de la app; NumberTicker anima el salto entre valores en
 * vez de solo reemplazar el texto, que es lo que le da sensación "viva".
 */
export function StatsBar({ status, stats, inicioMs, maxGeneraciones }: StatsBarProps) {
  const [ahora, setAhora] = useState(() => Date.now())
  const ultimaAptitudRef = useRef<number | null>(null)
  const [destello, setDestello] = useState(false)

  useEffect(() => {
    if (status !== 'running' && status !== 'paused') return
    const id = setInterval(() => setAhora(Date.now()), 1000)
    return () => clearInterval(id)
  }, [status])

  useEffect(() => {
    if (!stats) return
    if (ultimaAptitudRef.current !== null && stats.mejor_aptitud > ultimaAptitudRef.current) {
      setDestello(true)
      const t = setTimeout(() => setDestello(false), 200)
      return () => clearTimeout(t)
    }
    ultimaAptitudRef.current = stats.mejor_aptitud
  }, [stats])

  const transcurridoMs = inicioMs ? ahora - inicioMs : 0

  return (
    <div className="stats-menu">
      <div className="stats-menu-cabecera">
        <span className={`badge badge-${status}`}>{ETIQUETAS_ESTADO[status]}</span>
        <span className="stats-menu-tiempo">{formatearTiempo(transcurridoMs)}</span>
      </div>

      <div className="stats-menu-cuerpo">
        <GenerationCounter generacion={stats?.generacion ?? 0} maxGeneraciones={maxGeneraciones} />

        <div className="stats-menu-tiles">
          <StatTile
            label="Mejor aptitud"
            valor={<NumberTicker value={stats?.mejor_aptitud ?? 0} decimalPlaces={4} />}
            tono="verde"
            destello={destello}
          />
          <StatTile
            label="Aptitud promedio"
            valor={<NumberTicker value={stats?.aptitud_promedio ?? 0} decimalPlaces={4} />}
            tono="azul"
          />
          <StatTile
            label="Desv. macros"
            valor={<NumberTicker value={stats?.pen_macro ?? 0} decimalPlaces={3} />}
            tono="naranja"
          />
          <StatTile
            label="Desv. costo"
            valor={<NumberTicker value={stats?.pen_costo ?? 0} decimalPlaces={3} />}
            tono="naranja"
          />
          <StatTile label="Sin mejora" valor={stats?.generaciones_sin_mejora ?? 0} unidad="gen." />
        </div>
      </div>
    </div>
  )
}
