// Tipos compartidos del contrato de API del backend (Algoritmo Genético - TSP).

export type Seleccion = 'proporcional' | 'torneo' | 'estocastica' | 'heuristica'
export type Cruce = 'un_punto' | 'dos_puntos' | 'uniforme'
export type Mutacion = 'heuristica' | 'intercambio' | 'desplazamiento' | 'insercion'
export type CriterioParada = 'generaciones' | 'convergencia' | 'objetivo'
export type OrigenCiudades = 'aleatorio' | 'metro_medellin'

/** Una ciudad del mapa: coordenadas [x, y] normalizadas en [0,1]. */
export type Ciudad = [number, number]

/** Parámetros de configuración del algoritmo genético, enviados al backend al iniciar una corrida. */
export interface ParametrosAG {
  poblacion: number
  num_ciudades: number
  origen_ciudades: OrigenCiudades
  prob_cruce: number
  prob_mutacion: number
  elitismo: number
  seleccion: Seleccion
  k_torneo: number
  num_mejores: number
  cruce: Cruce
  mutacion: Mutacion
  criterio_parada: CriterioParada
  max_generaciones: number
  epsilon: number
  paciencia: number
  distancia_objetivo: number
  semilla_ciudades: number | null
  seed: number | null
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

// ---- Mensajes del WebSocket /ws/evolucion ----

/** Mensajes que el cliente envía al servidor. */
export type MensajeCliente =
  | { tipo: 'iniciar'; params: ParametrosAG }
  | { tipo: 'pausar' }
  | { tipo: 'reanudar' }
  | { tipo: 'detener' }

/** Mensajes que el servidor envía al cliente. */
export type MensajeServidor =
  | { tipo: 'iniciado'; run_id: string | number; ciudades: Ciudad[]; nombres_ciudades?: string[] }
  | {
      tipo: 'generacion'
      generacion: number
      mejor_aptitud: number
      aptitud_promedio: number
      aptitud_peor: number
      distancia_mejor: number
      distancia_promedio: number
      distancia_peor: number
      tiempo_ms: number
      generaciones_sin_mejora: number
      ruta_mejor: number[] | null
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
  distancia_mejor: number
  distancia_promedio: number
}

/** Últimas estadísticas conocidas de la corrida (para StatsBar). */
export interface EstadisticasActuales {
  generacion: number
  mejor_aptitud: number
  aptitud_promedio: number
  aptitud_peor: number
  distancia_mejor: number
  distancia_promedio: number
  distancia_peor: number
  generaciones_sin_mejora: number
  tiempo_ms: number
}
