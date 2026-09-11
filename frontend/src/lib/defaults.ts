import type { OpcionesParametros, ParametrosAG } from './tipos'

/**
 * Defaults y opciones hardcodeadas como fallback, usadas cuando
 * GET /api/parametros/opciones no responde (p. ej. backend aún no displegado).
 * Siempre se intenta primero el fetch real; esto es solo el respaldo.
 */
export const PARAMETROS_DEFAULT: ParametrosAG = {
  poblacion: 100,
  num_triangulos: 100,
  prob_cruce: 0.8,
  prob_mutacion: 0.05,
  elitismo: 2,
  seleccion: 'torneo',
  k_torneo: 3,
  cruce: 'un_punto',
  cruce_por_triangulo: true,
  mutacion: 'heuristica',
  sigma_mutacion: 0.1,
  criterio_parada: 'generaciones',
  max_generaciones: 2000,
  epsilon: 0.0001,
  paciencia: 100,
  aptitud_objetivo: 0.95,
  resolucion_trabajo: 128,
  seed: 42,
}

export const OPCIONES_PARAMETROS_FALLBACK: OpcionesParametros = {
  opciones: {
    seleccion: ['proporcional', 'torneo', 'estocastica', 'heuristica'],
    cruce: ['un_punto', 'dos_puntos', 'uniforme'],
    mutacion: ['heuristica', 'intercambio', 'desplazamiento', 'insercion'],
    criterio_parada: ['generaciones', 'convergencia', 'objetivo'],
  },
  defaults: PARAMETROS_DEFAULT,
}
