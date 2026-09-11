/** Descarga un array de filas como CSV. Cada fila es un array de celdas (string | number). */
export function descargarCsv(nombreArchivo: string, encabezados: string[], filas: (string | number)[][]): void {
  const escapar = (celda: string | number) => {
    const texto = String(celda)
    return /[",\n]/.test(texto) ? `"${texto.replace(/"/g, '""')}"` : texto
  }
  const lineas = [encabezados, ...filas].map((fila) => fila.map(escapar).join(','))
  const csv = lineas.join('\n')
  descargarBlob(new Blob([csv], { type: 'text/csv;charset=utf-8' }), nombreArchivo)
}

/** Descarga el contenido actual de un <canvas> como PNG. */
export function descargarCanvasComoPng(canvas: HTMLCanvasElement, nombreArchivo: string): void {
  canvas.toBlob((blob) => {
    if (blob) descargarBlob(blob, nombreArchivo)
  }, 'image/png')
}

function descargarBlob(blob: Blob, nombreArchivo: string): void {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = nombreArchivo
  a.click()
  URL.revokeObjectURL(url)
}
