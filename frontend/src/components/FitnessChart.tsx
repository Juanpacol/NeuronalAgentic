import { useEffect, useRef } from 'react'
import uPlot from 'uplot'
import 'uplot/dist/uPlot.min.css'
import type { PuntoHistoria } from '../lib/tipos'
import { Card } from './ui/Card'
import { Button } from './ui/Button'
import { descargarCanvasComoPng } from '../lib/exportar'

interface FitnessChartProps {
  historia: PuntoHistoria[]
  activo?: boolean
}

const ORO = '#f6d383'
const ROSA = '#d57ace'
const TEXTO_EJE = 'rgba(235, 235, 245, 0.6)'
const GRILLA = 'rgba(84, 84, 88, 0.35)'

/**
 * Relleno degradado bajo la línea de mejor aptitud: se desvanece de oro a
 * transparente. uPlot también invoca `fill` al inicializar la leyenda, antes
 * de tener `bbox` calculado — en ese caso cae a un color sólido.
 */
function degradadoOro(u: uPlot): CanvasGradient | string {
  if (!u.bbox || !(u.bbox.height > 0) || !Number.isFinite(u.bbox.top)) {
    return 'rgba(246, 211, 131, 0.2)'
  }
  const { ctx } = u
  const gradiente = ctx.createLinearGradient(0, u.bbox.top, 0, u.bbox.top + u.bbox.height)
  gradiente.addColorStop(0, 'rgba(246, 211, 131, 0.35)')
  gradiente.addColorStop(1, 'rgba(246, 211, 131, 0)')
  return gradiente
}

const OPCIONES_BASE: Omit<uPlot.Options, 'width' | 'height'> = {
  scales: { x: { time: false } },
  series: [
    {},
    {
      label: 'Mejor aptitud',
      stroke: ORO,
      width: 2.5,
      fill: degradadoOro,
      points: { show: true, size: 5, fill: ORO, stroke: ORO },
    },
    {
      label: 'Aptitud promedio',
      stroke: ROSA,
      width: 2,
      points: { show: true, size: 4, fill: ROSA, stroke: ROSA },
    },
  ],
  axes: [
    { label: 'Generación', stroke: TEXTO_EJE, grid: { stroke: GRILLA, width: 1 }, ticks: { stroke: GRILLA } },
    { label: 'Aptitud', stroke: TEXTO_EJE, grid: { stroke: GRILLA, width: 1 }, ticks: { stroke: GRILLA } },
  ],
}

/**
 * Gráfica de línea (uPlot) con mejor aptitud y aptitud promedio por
 * generación. Colores de "The Cheshire Diet" (oro/rosa) con relleno
 * degradado bajo la mejor línea; antes usaba el tema claro por defecto de
 * uPlot sobre el fondo negro de la app, casi ilegible.
 */
export function FitnessChart({ historia, activo }: FitnessChartProps) {
  const contenedorRef = useRef<HTMLDivElement | null>(null)
  const plotRef = useRef<uPlot | null>(null)

  useEffect(() => {
    const contenedor = contenedorRef.current
    if (!contenedor) return

    const rect = contenedor.getBoundingClientRect()
    const plot = new uPlot(
      { ...OPCIONES_BASE, width: rect.width || 600, height: 260 },
      [[], [], []],
      contenedor,
    )
    plotRef.current = plot

    const resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0]
      if (!entry) return
      // Ancho 0 pasa durante transiciones de layout (p. ej. el sidebar
      // cerrándose): con eso uPlot calcula escalas no finitas y explota al
      // dibujar. Se ignora ese frame transitorio en vez de pasárselo.
      const width = entry.contentRect.width
      if (width <= 0) return
      plot.setSize({ width, height: 260 })
    })
    resizeObserver.observe(contenedor)

    return () => {
      resizeObserver.disconnect()
      plot.destroy()
      plotRef.current = null
    }
  }, [])

  useEffect(() => {
    const plot = plotRef.current
    if (!plot) return
    const xs = historia.map((p) => p.generacion)
    const mejor = historia.map((p) => p.mejor_aptitud)
    const promedio = historia.map((p) => p.aptitud_promedio)
    plot.setData([xs, mejor, promedio])
  }, [historia])

  function handleDescargar() {
    const canvas = plotRef.current?.ctx.canvas
    if (canvas) descargarCanvasComoPng(canvas, 'the-cheshire-diet-aptitud.png')
  }

  return (
    <Card
      titulo="Evolución de la aptitud"
      subtitulo="Mejor dieta (oro) y promedio de la población (rosa) por generación."
      acento="rosa"
      className={activo ? 'fitness-chart-card fitness-chart-viva' : 'fitness-chart-card'}
    >
      <div ref={contenedorRef} className="fitness-chart" />
      <div className="dieta-descarga">
        <Button variant="tinted" tono="rosa" onClick={handleDescargar} disabled={historia.length === 0}>
          Descargar gráfica (PNG)
        </Button>
      </div>
    </Card>
  )
}
