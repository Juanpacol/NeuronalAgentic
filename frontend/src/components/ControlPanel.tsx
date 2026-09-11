import type { ChangeEvent } from 'react'
import type {
  CriterioParada,
  Cruce,
  EstadoConexion,
  Mutacion,
  OpcionesParametros,
  ParametrosAG,
  Seleccion,
  TargetInfo,
} from '../lib/tipos'

interface ControlPanelProps {
  params: ParametrosAG
  onChange: (params: ParametrosAG) => void
  opciones: OpcionesParametros['opciones']
  status: EstadoConexion
  targets: TargetInfo[]
  targetId: string
  onTargetIdChange: (id: string) => void
  onIniciar: () => void
  onPausar: () => void
  onReanudar: () => void
  onDetener: () => void
}

/** Panel de controles: todos los parámetros del AG + botones de ciclo de vida de la corrida. */
export function ControlPanel({
  params,
  onChange,
  opciones,
  status,
  targets,
  targetId,
  onTargetIdChange,
  onIniciar,
  onPausar,
  onReanudar,
  onDetener,
}: ControlPanelProps) {
  const deshabilitado = status === 'running'

  function actualizar<K extends keyof ParametrosAG>(campo: K, valor: ParametrosAG[K]) {
    onChange({ ...params, [campo]: valor })
  }

  function numero(e: ChangeEvent<HTMLInputElement>): number {
    return e.target.valueAsNumber
  }

  const puedeIniciar =
    status === 'idle' || status === 'open' || status === 'error'
  const puedePausar = status === 'running'
  const puedeReanudar = status === 'paused'
  const puedeDetener = status === 'running' || status === 'paused'

  return (
    <div className="control-panel">
      <fieldset disabled={deshabilitado}>
        <legend>Parámetros del algoritmo genético</legend>

        <label>
          Población
          <input
            type="number"
            min={1}
            value={params.poblacion}
            onChange={(e) => actualizar('poblacion', numero(e))}
          />
        </label>

        <label>
          Número de triángulos
          <input
            type="number"
            min={1}
            value={params.num_triangulos}
            onChange={(e) => actualizar('num_triangulos', numero(e))}
          />
        </label>

        <label>
          Prob. de cruce ({params.prob_cruce.toFixed(2)})
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={params.prob_cruce}
            onChange={(e) => actualizar('prob_cruce', numero(e))}
          />
        </label>

        <label>
          Prob. de mutación ({params.prob_mutacion.toFixed(2)})
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={params.prob_mutacion}
            onChange={(e) => actualizar('prob_mutacion', numero(e))}
          />
        </label>

        <label>
          Elitismo
          <input
            type="number"
            min={0}
            value={params.elitismo}
            onChange={(e) => actualizar('elitismo', numero(e))}
          />
        </label>

        <label>
          Selección
          <select
            value={params.seleccion}
            onChange={(e) => actualizar('seleccion', e.target.value as Seleccion)}
          >
            {opciones.seleccion.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </label>

        {params.seleccion === 'torneo' && (
          <label>
            k (torneo)
            <input
              type="number"
              min={2}
              value={params.k_torneo}
              onChange={(e) => actualizar('k_torneo', numero(e))}
            />
          </label>
        )}

        <label>
          Cruce
          <select value={params.cruce} onChange={(e) => actualizar('cruce', e.target.value as Cruce)}>
            {opciones.cruce.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </label>

        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={params.cruce_por_triangulo}
            onChange={(e) => actualizar('cruce_por_triangulo', e.target.checked)}
          />
          Cruce por triángulo
        </label>

        <label>
          Mutación
          <select
            value={params.mutacion}
            onChange={(e) => actualizar('mutacion', e.target.value as Mutacion)}
          >
            {opciones.mutacion.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </label>

        <label>
          Sigma de mutación
          <input
            type="number"
            min={0}
            step={0.01}
            value={params.sigma_mutacion}
            onChange={(e) => actualizar('sigma_mutacion', numero(e))}
          />
        </label>

        <label>
          Criterio de parada
          <select
            value={params.criterio_parada}
            onChange={(e) => actualizar('criterio_parada', e.target.value as CriterioParada)}
          >
            {opciones.criterio_parada.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </label>

        {params.criterio_parada === 'generaciones' && (
          <label>
            Máx. generaciones
            <input
              type="number"
              min={1}
              value={params.max_generaciones}
              onChange={(e) => actualizar('max_generaciones', numero(e))}
            />
          </label>
        )}

        {params.criterio_parada === 'convergencia' && (
          <>
            <label>
              Epsilon
              <input
                type="number"
                min={0}
                step={0.0001}
                value={params.epsilon}
                onChange={(e) => actualizar('epsilon', numero(e))}
              />
            </label>
            <label>
              Paciencia (generaciones sin mejora)
              <input
                type="number"
                min={1}
                value={params.paciencia}
                onChange={(e) => actualizar('paciencia', numero(e))}
              />
            </label>
          </>
        )}

        {params.criterio_parada === 'objetivo' && (
          <label>
            Aptitud objetivo
            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={params.aptitud_objetivo}
              onChange={(e) => actualizar('aptitud_objetivo', numero(e))}
            />
          </label>
        )}

        <label>
          Resolución de trabajo (px)
          <input
            type="number"
            min={16}
            value={params.resolucion_trabajo}
            onChange={(e) => actualizar('resolucion_trabajo', numero(e))}
          />
        </label>

        <label>
          Seed
          <input
            type="number"
            value={params.seed}
            onChange={(e) => actualizar('seed', numero(e))}
          />
        </label>

        {targets.length > 0 && (
          <label>
            Imagen objetivo
            <select value={targetId} onChange={(e) => onTargetIdChange(e.target.value)}>
              {targets.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.nombre}
                </option>
              ))}
            </select>
          </label>
        )}
      </fieldset>

      <div className="button-row">
        <button type="button" onClick={onIniciar} disabled={!puedeIniciar}>
          Iniciar
        </button>
        <button type="button" onClick={onPausar} disabled={!puedePausar}>
          Pausar
        </button>
        <button type="button" onClick={onReanudar} disabled={!puedeReanudar}>
          Reanudar
        </button>
        <button type="button" onClick={onDetener} disabled={!puedeDetener}>
          Detener
        </button>
      </div>
    </div>
  )
}
