import { OPCIONES_PARAMETROS_FALLBACK } from './defaults'
import type { CriterioParada, OpcionesParametros, ParametrosAG, TargetInfo } from './tipos'

const CRITERIOS_PARADA: CriterioParada[] = ['generaciones', 'convergencia', 'objetivo']

/**
 * Forma real de GET /api/parametros/opciones en el backend: plana, sin envoltorio
 * "opciones" y sin lista de criterios de parada (son un enum fijo, no configurable
 * del lado del servidor). Se adapta aquí a la forma que espera el resto del frontend.
 */
interface OpcionesBackendCrudo {
  seleccion: OpcionesParametros['opciones']['seleccion']
  cruce: OpcionesParametros['opciones']['cruce']
  mutacion: OpcionesParametros['opciones']['mutacion']
  defaults: ParametrosAG & { seed: number | null }
}

function adaptarOpciones(crudo: OpcionesBackendCrudo): OpcionesParametros {
  return {
    opciones: {
      seleccion: crudo.seleccion,
      cruce: crudo.cruce,
      mutacion: crudo.mutacion,
      criterio_parada: CRITERIOS_PARADA,
    },
    defaults: {
      ...crudo.defaults,
      seed: crudo.defaults.seed ?? 42,
    },
  }
}

export const API_URL: string =
  (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export const WS_URL: string =
  (import.meta.env.VITE_WS_URL as string | undefined) ?? 'ws://localhost:8000/ws/evolucion'

/**
 * Dispara un GET /health silencioso, ignorando el resultado.
 * Sirve solo para "despertar" un backend dormido (p. ej. en Render free tier)
 * mientras el usuario llena el formulario. Nunca debe lanzar ni bloquear.
 */
export function precalentarBackend(): void {
  fetch(`${API_URL}/health`).catch(() => {
    /* ignorado intencionalmente */
  })
}

/**
 * Obtiene las opciones/defaults de parámetros del backend.
 * Si falla (backend no disponible), retorna el fallback hardcodeado.
 */
export async function obtenerOpcionesParametros(): Promise<OpcionesParametros> {
  try {
    const res = await fetch(`${API_URL}/api/parametros/opciones`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = (await res.json()) as OpcionesBackendCrudo
    return adaptarOpciones(data)
  } catch {
    return OPCIONES_PARAMETROS_FALLBACK
  }
}

/**
 * Obtiene la lista de targets disponibles en el servidor.
 * Si falla, retorna una lista vacía (la app sigue funcionando con /target.jpg local).
 */
export async function obtenerTargets(): Promise<TargetInfo[]> {
  try {
    const res = await fetch(`${API_URL}/api/targets`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = (await res.json()) as TargetInfo[]
    return data
  } catch {
    return []
  }
}
