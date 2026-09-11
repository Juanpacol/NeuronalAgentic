import type { Ciudad } from './tipos'

const EXPORT_WIDTH = 1920
const EXPORT_HEIGHT = 1080

/**
 * Dibuja el mapa de ciudades y la ruta actual sobre un contexto ya escalado
 * a coordenadas [0,1] (ver setTransform en RouteCanvas/exportarRutaComoPng).
 */
export function dibujarRuta(
  ctx: CanvasRenderingContext2D,
  ciudades: Ciudad[],
  ruta: number[] | null,
): void {
  if (ruta && ruta.length > 1) {
    ctx.beginPath()
    const [x0, y0] = ciudades[ruta[0]]
    ctx.moveTo(x0, y0)
    for (let i = 1; i < ruta.length; i++) {
      const [x, y] = ciudades[ruta[i]]
      ctx.lineTo(x, y)
    }
    ctx.closePath() // vuelve a la ciudad de inicio (ciclo cerrado)
    ctx.strokeStyle = '#3498db'
    ctx.lineWidth = 0.004
    ctx.stroke()
  }

  // ciudades como puntos, encima de la ruta
  for (const [x, y] of ciudades) {
    ctx.beginPath()
    ctx.arc(x, y, 0.009, 0, Math.PI * 2)
    ctx.fillStyle = '#e74c3c'
    ctx.fill()
  }
}

/** Renderiza el mapa + ruta a un PNG offscreen a resolución fija y lo descarga. */
export function exportarRutaComoPng(
  ciudades: Ciudad[],
  ruta: number[] | null,
  nombreArchivo = 'ruta.png',
): void {
  const canvas = document.createElement('canvas')
  canvas.width = EXPORT_WIDTH
  canvas.height = EXPORT_HEIGHT
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.setTransform(canvas.width, 0, 0, canvas.height, 0, 0)
  ctx.fillStyle = '#0d1b2a'
  ctx.fillRect(0, 0, 1, 1)
  dibujarRuta(ctx, ciudades, ruta)
  ctx.setTransform(1, 0, 0, 1, 0, 0)

  canvas.toBlob((blob) => {
    if (!blob) return
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = nombreArchivo
    a.click()
    URL.revokeObjectURL(url)
  }, 'image/png')
}
