type Suscriptor = (mensajes: string[]) => void

const mensajes: string[] = []
const suscriptores = new Set<Suscriptor>()
let registrado = false

function publicar(mensaje: string) {
  mensajes.push(mensaje)
  // Solo interesan los últimos; una ráfaga de errores no debe crecer sin límite.
  if (mensajes.length > 5) mensajes.shift()
  for (const s of suscriptores) s([...mensajes])
}

/** Captura errores que ningún ErrorBoundary puede ver: async, promesas, listeners. */
export function registrarListenersGlobales() {
  if (registrado) return
  registrado = true

  window.addEventListener('error', (e) => {
    publicar(e.message || 'Error desconocido')
  })

  window.addEventListener('unhandledrejection', (e) => {
    const razon = e.reason
    publicar(razon instanceof Error ? razon.message : String(razon))
  })
}

export function suscribirseAErrores(suscriptor: Suscriptor): () => void {
  suscriptores.add(suscriptor)
  return () => {
    suscriptores.delete(suscriptor)
  }
}

export function limpiarErroresGlobales() {
  mensajes.length = 0
  for (const s of suscriptores) s([])
}

/** Para reportar manualmente desde un catch (p. ej. el onmessage del WebSocket). */
export function reportarError(mensaje: string) {
  publicar(mensaje)
}
