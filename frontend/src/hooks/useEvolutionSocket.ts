import { useCallback, useEffect, useRef, useState, type RefObject } from 'react'
import type {
  Alimento,
  EstadisticasActuales,
  EstadoConexion,
  MensajeCliente,
  MensajeServidor,
  ObjetivosDieta,
  ParametrosAG,
  PuntoHistoria,
} from '../lib/tipos'

const MAX_INTENTOS_RECONEXION = 5
const BACKOFF_BASE_MS = 1000 // 1, 2, 4, 8, 16s
const THROTTLE_MS = 120 // ~8Hz
const TIEMPO_WAKING_MS = 3000
const TIEMPO_ERROR_MS = 90000

interface UseEvolutionSocketResult {
  status: EstadoConexion
  stats: EstadisticasActuales | null
  historia: PuntoHistoria[]
  alimentosRef: RefObject<Alimento[]>
  genomaRef: RefObject<number[] | null>
  objetivosRef: RefObject<ObjetivosDieta | null>
  iniciar: (params: ParametrosAG) => void
  pausar: () => void
  reanudar: () => void
  detener: () => void
  mensajeError: string | null
}

export function useEvolutionSocket(wsUrl: string): UseEvolutionSocketResult {
  const [status, setStatus] = useState<EstadoConexion>('idle')
  const [stats, setStats] = useState<EstadisticasActuales | null>(null)
  const [historia, setHistoria] = useState<PuntoHistoria[]>([])
  const [mensajeError, setMensajeError] = useState<string | null>(null)

  const alimentosRef = useRef<Alimento[]>([])
  const genomaRef = useRef<number[] | null>(null)
  const objetivosRef = useRef<ObjetivosDieta | null>(null)
  const socketRef = useRef<WebSocket | null>(null)
  const intentosRef = useRef(0)
  const corridaActivaRef = useRef(false)
  const ultimosParamsRef = useRef<{ params: ParametrosAG } | null>(null)

  // Buffers pendientes de volcarse a React a ~8Hz.
  const statsPendientesRef = useRef<EstadisticasActuales | null>(null)
  const historiaPendienteRef = useRef<PuntoHistoria[]>([])
  const sucioRef = useRef(false)

  const wakingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const errorTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const reconexionTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const flushIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const limpiarTimers = useCallback(() => {
    if (wakingTimeoutRef.current) clearTimeout(wakingTimeoutRef.current)
    if (errorTimeoutRef.current) clearTimeout(errorTimeoutRef.current)
    if (reconexionTimeoutRef.current) clearTimeout(reconexionTimeoutRef.current)
    wakingTimeoutRef.current = null
    errorTimeoutRef.current = null
    reconexionTimeoutRef.current = null
  }, [])

  // Loop de volcado throttled ~8Hz: aplica los últimos stats + historia acumulada.
  useEffect(() => {
    flushIntervalRef.current = setInterval(() => {
      if (!sucioRef.current) return
      sucioRef.current = false
      if (statsPendientesRef.current) {
        setStats(statsPendientesRef.current)
      }
      if (historiaPendienteRef.current.length > 0) {
        const nuevos = historiaPendienteRef.current
        historiaPendienteRef.current = []
        setHistoria((prev) => [...prev, ...nuevos])
      }
    }, THROTTLE_MS)
    return () => {
      if (flushIntervalRef.current) clearInterval(flushIntervalRef.current)
    }
  }, [])

  const enviar = useCallback((msg: MensajeCliente) => {
    const ws = socketRef.current
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg))
    }
  }, [])

  const cerrarSocket = useCallback(() => {
    const ws = socketRef.current
    socketRef.current = null
    if (ws) {
      ws.onopen = null
      ws.onmessage = null
      ws.onclose = null
      ws.onerror = null
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close()
      }
    }
  }, [])

  const conectar = useCallback(
    (esReconexion: boolean) => {
      limpiarTimers()
      setStatus(esReconexion ? 'reconnecting' : 'connecting')
      setMensajeError(null)

      let socket: WebSocket
      try {
        socket = new WebSocket(wsUrl)
      } catch {
        setStatus('error')
        setMensajeError('No se pudo abrir la conexión WebSocket.')
        return
      }
      socketRef.current = socket

      // Si no hay onopen en 3s, probablemente el backend (Render free) está dormido.
      wakingTimeoutRef.current = setTimeout(() => {
        setStatus((prev) => (prev === 'connecting' || prev === 'reconnecting' ? 'waking' : prev))
      }, TIEMPO_WAKING_MS)

      // Si tras 90s no se ha conseguido conectar, mostramos error definitivo.
      errorTimeoutRef.current = setTimeout(() => {
        setStatus((prev) => {
          if (prev === 'open' || prev === 'running' || prev === 'paused') return prev
          setMensajeError('El servidor no respondió a tiempo. Intenta de nuevo.')
          cerrarSocket()
          return 'error'
        })
      }, TIEMPO_ERROR_MS)

      socket.onopen = () => {
        if (wakingTimeoutRef.current) clearTimeout(wakingTimeoutRef.current)
        if (errorTimeoutRef.current) clearTimeout(errorTimeoutRef.current)
        intentosRef.current = 0
        setStatus('open')

        // Si esto es una reconexión durante una corrida activa, reinicia con los últimos params.
        if (esReconexion && corridaActivaRef.current && ultimosParamsRef.current) {
          const { params } = ultimosParamsRef.current
          enviar({ tipo: 'iniciar', params })
        }
      }

      socket.onmessage = (event: MessageEvent<string>) => {
        let msg: MensajeServidor
        try {
          msg = JSON.parse(event.data) as MensajeServidor
        } catch {
          return
        }

        switch (msg.tipo) {
          case 'iniciado': {
            corridaActivaRef.current = true
            alimentosRef.current = msg.alimentos
            objetivosRef.current = msg.objetivos
            genomaRef.current = null
            setStatus('running')
            break
          }
          case 'generacion': {
            if (msg.genoma_mejor) {
              genomaRef.current = msg.genoma_mejor
            }
            const punto: EstadisticasActuales = {
              generacion: msg.generacion,
              mejor_aptitud: msg.mejor_aptitud,
              aptitud_promedio: msg.aptitud_promedio,
              aptitud_peor: msg.aptitud_peor,
              costo_mejor: msg.costo_mejor,
              pen_macro: msg.pen_macro,
              pen_costo: msg.pen_costo,
              macros_mejor: msg.macros_mejor,
              generaciones_sin_mejora: msg.generaciones_sin_mejora,
              tiempo_ms: msg.tiempo_ms,
            }
            statsPendientesRef.current = punto
            historiaPendienteRef.current.push({
              generacion: msg.generacion,
              mejor_aptitud: msg.mejor_aptitud,
              aptitud_promedio: msg.aptitud_promedio,
              aptitud_peor: msg.aptitud_peor,
              costo_mejor: msg.costo_mejor,
              pen_macro: msg.pen_macro,
              pen_costo: msg.pen_costo,
            })
            sucioRef.current = true
            break
          }
          case 'finalizado': {
            corridaActivaRef.current = false
            setStatus('open')
            break
          }
          case 'error': {
            if (msg.codigo === 'capacidad') {
              setMensajeError('El servidor está sobrecargado. Intenta de nuevo en unos minutos.')
            } else {
              setMensajeError(`Error del servidor: ${msg.codigo}`)
            }
            setStatus('error')
            corridaActivaRef.current = false
            break
          }
        }
      }

      socket.onerror = () => {
        // El evento close se dispara después; el manejo real ocurre en onclose.
      }

      socket.onclose = () => {
        if (wakingTimeoutRef.current) clearTimeout(wakingTimeoutRef.current)
        if (errorTimeoutRef.current) clearTimeout(errorTimeoutRef.current)
        socketRef.current = null

        if (corridaActivaRef.current && intentosRef.current < MAX_INTENTOS_RECONEXION) {
          const intento = intentosRef.current
          intentosRef.current += 1
          const espera = BACKOFF_BASE_MS * Math.pow(2, intento)
          setStatus('reconnecting')
          reconexionTimeoutRef.current = setTimeout(() => {
            conectar(true)
          }, espera)
        } else if (corridaActivaRef.current) {
          corridaActivaRef.current = false
          setMensajeError('Se perdió la conexión y se agotaron los intentos de reconexión.')
          setStatus('error')
        } else {
          setStatus((prev) => (prev === 'error' ? prev : 'idle'))
        }
      }
    },
    [wsUrl, enviar, cerrarSocket, limpiarTimers],
  )

  const iniciar = useCallback(
    (params: ParametrosAG) => {
      ultimosParamsRef.current = { params }
      corridaActivaRef.current = true
      intentosRef.current = 0
      genomaRef.current = null
      setHistoria([])
      setStats(null)
      historiaPendienteRef.current = []
      statsPendientesRef.current = null

      const ws = socketRef.current
      if (ws && ws.readyState === WebSocket.OPEN) {
        enviar({ tipo: 'iniciar', params })
      } else {
        conectar(false)
        // El envío real de "iniciar" ocurre en onopen si fue reconexión;
        // para el primer arranque lo enviamos aquí en cuanto abra.
        const esperarYEnviar = () => {
          const s = socketRef.current
          if (s && s.readyState === WebSocket.OPEN) {
            enviar({ tipo: 'iniciar', params })
          } else if (s && s.readyState === WebSocket.CONNECTING) {
            setTimeout(esperarYEnviar, 50)
          }
        }
        setTimeout(esperarYEnviar, 50)
      }
    },
    [conectar, enviar],
  )

  const pausar = useCallback(() => {
    enviar({ tipo: 'pausar' })
    setStatus('paused')
  }, [enviar])

  const reanudar = useCallback(() => {
    enviar({ tipo: 'reanudar' })
    setStatus('running')
  }, [enviar])

  const detener = useCallback(() => {
    corridaActivaRef.current = false
    enviar({ tipo: 'detener' })
    cerrarSocket()
    limpiarTimers()
    setStatus('idle')
  }, [enviar, cerrarSocket, limpiarTimers])

  useEffect(() => {
    return () => {
      corridaActivaRef.current = false
      limpiarTimers()
      cerrarSocket()
    }
  }, [cerrarSocket, limpiarTimers])

  return {
    status,
    stats,
    historia,
    alimentosRef,
    genomaRef,
    objetivosRef,
    iniciar,
    pausar,
    reanudar,
    detener,
    mensajeError,
  }
}
