import { useEffect, useState } from 'react'
import { limpiarErroresGlobales, suscribirseAErrores } from '../lib/errores'

/** Aviso flotante, no bloqueante, para errores asíncronos. La aplicación sigue usable. */
export function AvisoErroresGlobales() {
  const [lista, setLista] = useState<string[]>([])

  useEffect(() => suscribirseAErrores(setLista), [])

  if (lista.length === 0) return null

  return (
    <div className="aviso-errores" role="alert">
      <div className="aviso-errores-cuerpo">
        <strong>Error en segundo plano</strong>
        <ul>
          {lista.map((m, i) => (
            <li key={`${m}-${i}`}>{m}</li>
          ))}
        </ul>
      </div>
      <button type="button" onClick={limpiarErroresGlobales} aria-label="Cerrar aviso">
        ✕
      </button>
    </div>
  )
}
