// Tipos compartidos del contrato de API del backend (Algoritmo Genético - Dieta).

export type Seleccion = 'proporcional' | 'torneo' | 'estocastica' | 'heuristica'
export type Cruce = 'un_punto' | 'dos_puntos' | 'uniforme'
export type Mutacion = 'heuristica' | 'intercambio' | 'desplazamiento' | 'insercion'
export type CriterioParada = 'generaciones' | 'convergencia' | 'objetivo'

/** Un alimento del catálogo, tal como lo sirve GET/`iniciado` (ver alimentos.py). */
export interface Alimento {
  codigo_tcac: string
  nombre: string
  categoria: string
  unidad: string
  gramos_porcion: number
  kcal: number
  proteina_g: number
  carbohidratos_g: number
  grasa_g: number
  precio_cop: number
  precio_verificado: boolean
  max_porciones: number
  fuente: string
}

/** Metas nutricionales/presupuesto enviadas de vuelta por el backend al iniciar. */
export interface ObjetivosDieta {
  kcal: number
  proteina_g: number
  carbohidratos_g: number
  grasa_g: number
  presupuesto_cop: number
}

/** Macros totales aportados por la mejor dieta de la generación actual. */
export interface MacrosDieta {
  kcal: number
  proteina_g: number
  carbohidratos_g: number
  grasa_g: number
}

/** Parámetros de configuración del algoritmo genético, enviados al backend al iniciar una corrida. */
export interface ParametrosAG {
  poblacion: number
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
  aptitud_objetivo: number
  objetivo_kcal: number
  objetivo_proteina_g: number
  objetivo_carbohidratos_g: number
  objetivo_grasa_g: number
  peso_costo: number
  presupuesto_cop: number
  seed: number | null
  retardo_ms: number
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
  | { tipo: 'iniciado'; run_id: string; alimentos: Alimento[]; objetivos: ObjetivosDieta }
  | {
      tipo: 'generacion'
      generacion: number
      mejor_aptitud: number
      aptitud_promedio: number
      aptitud_peor: number
      costo_mejor: number
      desviacion_mejor: number
      pen_macro: number
      pen_costo: number
      macros_mejor: MacrosDieta
      aptitudes: number[]
      tiempo_ms: number
      generaciones_sin_mejora: number
      genoma_mejor?: number[]
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
  costo_mejor: number
  pen_macro: number
  pen_costo: number
}

/** Últimas estadísticas conocidas de la corrida (para StatsBar). */
export interface EstadisticasActuales {
  generacion: number
  mejor_aptitud: number
  aptitud_promedio: number
  aptitud_peor: number
  costo_mejor: number
  pen_macro: number
  pen_costo: number
  macros_mejor: MacrosDieta
  generaciones_sin_mejora: number
  tiempo_ms: number
}
