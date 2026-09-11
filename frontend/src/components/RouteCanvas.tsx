import { useEffect, useRef, type RefObject } from 'react'
import type { Ciudad } from '../lib/tipos'
import { dibujarRuta } from '../lib/canvas'

interface RouteCanvasProps {
  ciudadesRef: RefObject<Ciudad[]>
  rutaRef: RefObject<number[] | null>
}

/**
 * Canvas 2D que dibuja el mapa de ciudades y la mejor ruta de la generación actual.
 * Recibe refs (no estado) para no forzar re-renders de React en cada generación;
 * usa su propio loop de requestAnimationFrame y solo redibuja cuando la ruta cambió.
 */
export function RouteCanvas({ ciudadesRef, rutaRef }: RouteCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const ultimaDibujadaRef = useRef<number[] | null>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const contenedor = canvas.parentElement
    if (!contenedor) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    function redimensionar() {
      const dpr = window.devicePixelRatio || 1
      const rect = contenedor!.getBoundingClientRect()
      const ancho = Math.max(1, Math.round(rect.width * dpr))
      const alto = Math.max(1, Math.round((rect.width * 9) / 16 * dpr))
      if (canvas!.width !== ancho || canvas!.height !== alto) {
        canvas!.width = ancho
        canvas!.height = alto
      }
      ultimaDibujadaRef.current = null // fuerza redibujo tras resize
    }

    const resizeObserver = new ResizeObserver(redimensionar)
    resizeObserver.observe(contenedor)
    redimensionar()

    let frameId: number

    function loop() {
      const actual = rutaRef.current
      if (actual !== ultimaDibujadaRef.current) {
        ultimaDibujadaRef.current = actual
        // Truco de escalado: tras dimensionar el canvas, permite dibujar
        // directamente con coordenadas normalizadas [0,1].
        ctx!.setTransform(canvas!.width, 0, 0, canvas!.height, 0, 0)
        ctx!.fillStyle = '#0d1b2a'
        ctx!.fillRect(0, 0, 1, 1)
        dibujarRuta(ctx!, ciudadesRef.current ?? [], actual)
      }
      frameId = requestAnimationFrame(loop)
    }
    frameId = requestAnimationFrame(loop)

    return () => {
      cancelAnimationFrame(frameId)
      resizeObserver.disconnect()
    }
  }, [ciudadesRef, rutaRef])

  return (
    <div className="canvas-box">
      <canvas ref={canvasRef} className="genome-canvas" />
    </div>
  )
}
