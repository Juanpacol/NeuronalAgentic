import { useEffect, useRef } from 'react'
import uPlot from 'uplot'
import 'uplot/dist/uPlot.min.css'
import type { PuntoHistoria } from '../lib/tipos'

interface FitnessChartProps {
  historia: PuntoHistoria[]
}

const OPCIONES_BASE: Omit<uPlot.Options, 'width' | 'height'> = {
  title: 'Aptitud por generación',
  scales: { x: { time: false } },
  series: [
    {},
    { label: 'Mejor aptitud', stroke: '#e74c3c', width: 2 },
    { label: 'Aptitud promedio', stroke: '#3498db', width: 2 },
  ],
  axes: [{ label: 'Generación' }, { label: 'Aptitud' }],
}

/** Gráfica de línea (uPlot) con mejor aptitud y aptitud promedio por generación. */
export function FitnessChart({ historia }: FitnessChartProps) {
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
      plot.setSize({ width: entry.contentRect.width, height: 260 })
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

  return <div ref={contenedorRef} className="fitness-chart" />
}
