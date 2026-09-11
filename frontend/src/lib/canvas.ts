import type { Triangulo } from './tipos'

const EXPORT_WIDTH = 1920
const EXPORT_HEIGHT = 1080

/** Dibuja los triángulos de un genoma sobre un contexto ya escalado a coordenadas [0,1]. */
export function dibujarTriangulos(ctx: CanvasRenderingContext2D, triangulos: Triangulo[]): void {
  for (const tri of triangulos) {
    const [p0, p1, p2] = tri.puntos
    const [r, g, b] = tri.color
    ctx.beginPath()
    ctx.moveTo(p0[0], p0[1])
    ctx.lineTo(p1[0], p1[1])
    ctx.lineTo(p2[0], p2[1])
    ctx.closePath()
    ctx.fillStyle = `rgba(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)}, ${tri.alpha})`
    ctx.fill()
  }
}

/** Renderiza un genoma (lista de triángulos) a un PNG offscreen a resolución fija y lo descarga. */
export function exportarGenomaComoPng(
  triangulos: Triangulo[] | null,
  nombreArchivo = 'genoma.png',
): void {
  const canvas = document.createElement('canvas')
  canvas.width = EXPORT_WIDTH
  canvas.height = EXPORT_HEIGHT
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.setTransform(canvas.width, 0, 0, canvas.height, 0, 0)
  ctx.fillStyle = '#000000'
  ctx.fillRect(0, 0, 1, 1)
  if (triangulos) {
    dibujarTriangulos(ctx, triangulos)
  }
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
