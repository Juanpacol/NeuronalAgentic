import type { OpcionesParametros, ParametrosAG } from './tipos'

/**
 * Defaults y opciones hardcodeadas como fallback, usadas cuando
 * GET /api/parametros/opciones no responde (p. ej. backend aún no displegado).
 * Siempre se intenta primero el fetch real; esto es solo el respaldo.
 */
export const PARAMETROS_DEFAULT: ParametrosAG = {
  poblacion: 50,
  num_triangulos: 110,
  prob_cruce: 0.7,
  prob_mutacion: 0.15,
  elitismo: 3,
  seleccion: 'torneo',
  k_torneo: 3,
  cruce: 'un_punto',
  cruce_por_triangulo: true,
  mutacion: 'heuristica',
  sigma_mutacion: 0.1,
  criterio_parada: 'generaciones',
  max_generaciones: 500,
  epsilon: 0.0005,
  paciencia: 30,
  aptitud_objetivo: 0.97,
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
