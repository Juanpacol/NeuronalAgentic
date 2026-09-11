import { useEffect, useRef, type RefObject } from 'react'
import type { Triangulo } from '../lib/tipos'
import { dibujarTriangulos } from '../lib/canvas'

interface GenomeCanvasProps {
  genomaRef: RefObject<Triangulo[] | null>
}

/**
 * Canvas 2D que dibuja el mejor genoma de la generación actual.
 * Recibe una ref (no estado) para no forzar re-renders de React en cada generación;
 * usa su propio loop de requestAnimationFrame y solo redibuja cuando el genoma cambió.
 */
export function GenomeCanvas({ genomaRef }: GenomeCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const ultimoDibujadoRef = useRef<Triangulo[] | null>(null)

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
      ultimoDibujadoRef.current = null // fuerza redibujo tras resize
    }

    const resizeObserver = new ResizeObserver(redimensionar)
    resizeObserver.observe(contenedor)
    redimensionar()

    let frameId: number

    function loop() {
      const actual = genomaRef.current
      if (actual !== ultimoDibujadoRef.current) {
        ultimoDibujadoRef.current = actual
        // Truco de escalado: tras dimensionar el canvas, permite dibujar
        // directamente con coordenadas normalizadas [0,1].
        ctx!.setTransform(canvas!.width, 0, 0, canvas!.height, 0, 0)
        ctx!.fillStyle = '#000000'
        ctx!.fillRect(0, 0, 1, 1)
        if (actual) {
          dibujarTriangulos(ctx!, actual)
        }
      }
      frameId = requestAnimationFrame(loop)
    }
    frameId = requestAnimationFrame(loop)

    return () => {
      cancelAnimationFrame(frameId)
      resizeObserver.disconnect()
    }
  }, [genomaRef])

  return (
    <div className="canvas-box">
      <canvas ref={canvasRef} className="genome-canvas" />
    </div>
  )
}
