import type { OpcionesParametros, ParametrosAG } from './tipos'

/**
 * Defaults y opciones hardcodeadas como fallback, usadas cuando
 * GET /api/parametros/opciones no responde (p. ej. backend aún no desplegado).
 * Siempre se intenta primero el fetch real; esto es solo el respaldo.
 */
export const PARAMETROS_DEFAULT: ParametrosAG = {
  poblacion: 60,
  num_ciudades: 30,
  prob_cruce: 0.85,
  prob_mutacion: 0.15,
  elitismo: 3,
  seleccion: 'torneo',
  k_torneo: 3,
  num_mejores: 10,
  cruce: 'dos_puntos',
  mutacion: 'heuristica',
  criterio_parada: 'generaciones',
  max_generaciones: 400,
  epsilon: 0.0005,
  paciencia: 40,
  distancia_objetivo: 5.0,
  semilla_ciudades: null,
  seed: null,
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
