// Tipos compartidos del contrato de API del backend (Algoritmo Genético).

export type Seleccion = 'proporcional' | 'torneo' | 'estocastica' | 'heuristica'
export type Cruce = 'un_punto' | 'dos_puntos' | 'uniforme'
export type Mutacion = 'heuristica' | 'intercambio' | 'desplazamiento' | 'insercion'
export type CriterioParada = 'generaciones' | 'convergencia' | 'objetivo'

/** Parámetros de configuración del algoritmo genético, enviados al backend al iniciar una corrida. */
export interface ParametrosAG {
  poblacion: number
  num_triangulos: number
  prob_cruce: number
  prob_mutacion: number
  elitismo: number
  seleccion: Seleccion
  k_torneo: number
  cruce: Cruce
  cruce_por_triangulo: boolean
  mutacion: Mutacion
  sigma_mutacion: number
  criterio_parada: CriterioParada
  max_generaciones: number
  epsilon: number
  paciencia: number
  aptitud_objetivo: number
  resolucion_trabajo: number
  seed: number
}

/** Respuesta de GET /api/parametros/opciones: opciones disponibles + defaults. */
export interface OpcionesParametros {
  opciones: {
    seleccion: Seleccion[]
    cruce: Cruce[]
    mutacion: Mutacion[]
    criterio_parada: CriterioParada[]
  }
  defaults: ParametrosAG
}

/** Un target disponible en el servidor, listado por GET /api/targets. */
export interface TargetInfo {
  id: string
  nombre: string
  url?: string
}

/** Un triángulo decodificado del genoma, con todos los valores normalizados en [0,1]. */
export interface Triangulo {
  puntos: [[number, number], [number, number], [number, number]]
  color: [number, number, number]
  alpha: number
}

// ---- Mensajes del WebSocket /ws/evolucion ----

/** Mensajes que el cliente envía al servidor. */
export type MensajeCliente =
  | { tipo: 'iniciar'; params: ParametrosAG; target_id: string }
  | { tipo: 'pausar' }
  | { tipo: 'reanudar' }
  | { tipo: 'detener' }

/** Mensajes que el servidor envía al cliente. */
export type MensajeServidor =
  | { tipo: 'iniciado'; run_id: string | number }
  | {
      tipo: 'generacion'
      generacion: number
      mejor_aptitud: number
      aptitud_promedio: number
      aptitud_peor: number
      tiempo_ms: number
      generaciones_sin_mejora: number
      genoma_mejor: Triangulo[] | null
    }
  | { tipo: 'finalizado'; razon: string; generaciones: number }
  | { tipo: 'error'; codigo: string }

/** Estado de la conexión/corrida expuesto por el hook useEvolutionSocket. */
export type EstadoConexion =
  | 'idle'
  | 'connecting'
  | 'waking'
  | 'open'
  | 'running'
  | 'paused'
  | 'reconnecting'
  | 'error'

/** Un punto de estadísticas de una generación, acumulado para historial/gráfica. */
export interface PuntoHistoria {
  generacion: number
  mejor_aptitud: number
  aptitud_promedio: number
  aptitud_peor: number
}

/** Últimas estadísticas conocidas de la corrida (para StatsBar). */
export interface EstadisticasActuales {
  generacion: number
  mejor_aptitud: number
  aptitud_promedio: number
  aptitud_peor: number
  generaciones_sin_mejora: number
  tiempo_ms: number
}
