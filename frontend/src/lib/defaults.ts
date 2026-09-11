import type { OpcionesParametros, ParametrosAG } from './tipos'

/**
 * Defaults y opciones hardcodeadas como fallback, usadas cuando
 * GET /api/parametros/opciones no responde (p. ej. backend aún no desplegado).
 * Siempre se intenta primero el fetch real; esto es solo el respaldo.
 */
export const PARAMETROS_DEFAULT: ParametrosAG = {
  poblacion: 80,
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
  aptitud_objetivo: 0.95,
  objetivo_kcal: 2000,
  objetivo_proteina_g: 75,
  objetivo_carbohidratos_g: 250,
  objetivo_grasa_g: 65,
  peso_costo: 0.5,
  presupuesto_cop: 20000,
  seed: null,
  retardo_ms: 0,
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
