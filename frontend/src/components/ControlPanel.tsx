import type {
  CriterioParada,
  Cruce,
  EstadoConexion,
  Mutacion,
  OpcionesParametros,
  ParametrosAG,
  Seleccion,
} from '../lib/tipos'
import { Card } from './ui/Card'
import { Slider } from './ui/Slider'
import { Stepper } from './ui/Stepper'
import { SegmentedControl, type OpcionSegmentada } from './ui/SegmentedControl'
import { Button } from './ui/Button'
import { ListRow } from './ui/ListRow'
import { CalculadoraMetas } from './CalculadoraMetas'

interface ControlPanelProps {
  params: ParametrosAG
  onChange: (params: ParametrosAG) => void
  opciones: OpcionesParametros['opciones']
  status: EstadoConexion
  onIniciar: () => void
  onPausar: () => void
  onReanudar: () => void
  onDetener: () => void
}

function comoOpciones<T extends string>(valores: readonly T[]): OpcionSegmentada<T>[] {
  return valores.map((v) => ({ valor: v, etiqueta: v }))
}

const FORMATO_COP = (v: number) => `$${v.toLocaleString('es-CO')}`
const FORMATO_PCT = (v: number) => `${(v * 100).toFixed(0)}%`

/** Panel de controles: metas de la dieta, parámetros del AG y ciclo de vida de la corrida. */
export function ControlPanel({
  params,
  onChange,
  opciones,
  status,
  onIniciar,
  onPausar,
  onReanudar,
  onDetener,
}: ControlPanelProps) {
  const deshabilitado = status === 'running'

  function actualizar<K extends keyof ParametrosAG>(campo: K, valor: ParametrosAG[K]) {
    onChange({ ...params, [campo]: valor })
  }

  const puedeIniciar = status === 'idle' || status === 'open' || status === 'error'
  const puedePausar = status === 'running'
  const puedeReanudar = status === 'paused'
  const puedeDetener = status === 'running' || status === 'paused'

  return (
    <div className="control-panel">
      <CalculadoraMetas
        disabled={deshabilitado}
        onAplicar={(metas) => onChange({ ...params, ...metas })}
      />

      <Card titulo="Metas nutricionales y presupuesto">
        <div className="control-panel-fila">
          <Slider
            label="Calorías"
            min={1000}
            max={4000}
            step={50}
            valor={params.objetivo_kcal}
            disabled={deshabilitado}
            formato={(v) => `${v} kcal`}
            onChange={(v) => actualizar('objetivo_kcal', v)}
          />
          <Slider
            label="Proteína"
            min={20}
            max={200}
            step={5}
            valor={params.objetivo_proteina_g}
            disabled={deshabilitado}
            formato={(v) => `${v} g`}
            onChange={(v) => actualizar('objetivo_proteina_g', v)}
          />
          <Slider
            label="Carbohidratos"
            min={50}
            max={500}
            step={10}
            valor={params.objetivo_carbohidratos_g}
            disabled={deshabilitado}
            formato={(v) => `${v} g`}
            onChange={(v) => actualizar('objetivo_carbohidratos_g', v)}
          />
          <Slider
            label="Grasa"
            min={20}
            max={200}
            step={5}
            valor={params.objetivo_grasa_g}
            disabled={deshabilitado}
            formato={(v) => `${v} g`}
            onChange={(v) => actualizar('objetivo_grasa_g', v)}
          />
          <Slider
            label="Presupuesto diario"
            min={2000}
            max={60000}
            step={1000}
            valor={params.presupuesto_cop}
            disabled={deshabilitado}
            formato={FORMATO_COP}
            onChange={(v) => actualizar('presupuesto_cop', v)}
          />
          <Slider
            label="Peso del costo vs. nutrición"
            min={0}
            max={1}
            step={0.01}
            valor={params.peso_costo}
            disabled={deshabilitado}
            formato={FORMATO_PCT}
            onChange={(v) => actualizar('peso_costo', v)}
          />
        </div>
      </Card>

      <Card titulo="Población y operadores">
        <div className="control-panel-fila">
          <Stepper
            label="Población"
            min={10}
            max={300}
            paso={10}
            valor={params.poblacion}
            disabled={deshabilitado}
            onChange={(v) => actualizar('poblacion', v)}
          />
          <Stepper
            label="Elitismo"
            min={0}
            max={20}
            valor={params.elitismo}
            disabled={deshabilitado}
            onChange={(v) => actualizar('elitismo', v)}
          />
          <Slider
            label="Prob. de cruce"
            min={0}
            max={1}
            step={0.01}
            valor={params.prob_cruce}
            disabled={deshabilitado}
            formato={FORMATO_PCT}
            onChange={(v) => actualizar('prob_cruce', v)}
          />
          <Slider
            label="Prob. de mutación"
            min={0}
            max={1}
            step={0.01}
            valor={params.prob_mutacion}
            disabled={deshabilitado}
            formato={FORMATO_PCT}
            onChange={(v) => actualizar('prob_mutacion', v)}
          />
        </div>

        <div className="control-panel-campo">
          <span className="ui-slider-label">Selección</span>
          <SegmentedControl
            opciones={comoOpciones(opciones.seleccion)}
            valor={params.seleccion}
            disabled={deshabilitado}
            onChange={(v: Seleccion) => actualizar('seleccion', v)}
          />
        </div>
        {params.seleccion === 'torneo' && (
          <Stepper
            label="k (torneo)"
            min={2}
            max={10}
            valor={params.k_torneo}
            disabled={deshabilitado}
            onChange={(v) => actualizar('k_torneo', v)}
          />
        )}
        {params.seleccion === 'heuristica' && (
          <Stepper
            label="Núm. mejores (truncamiento)"
            min={1}
            max={50}
            valor={params.num_mejores}
            disabled={deshabilitado}
            onChange={(v) => actualizar('num_mejores', v)}
          />
        )}

        <div className="control-panel-campo">
          <span className="ui-slider-label">Cruce</span>
          <SegmentedControl
            opciones={comoOpciones(opciones.cruce)}
            valor={params.cruce}
            disabled={deshabilitado}
            onChange={(v: Cruce) => actualizar('cruce', v)}
          />
        </div>

        <div className="control-panel-campo">
          <span className="ui-slider-label">Mutación</span>
          <SegmentedControl
            opciones={comoOpciones(opciones.mutacion)}
            valor={params.mutacion}
            disabled={deshabilitado}
            onChange={(v: Mutacion) => actualizar('mutacion', v)}
          />
        </div>
      </Card>

      <Card titulo="Criterio de parada">
        <div className="control-panel-campo">
          <span className="ui-slider-label">Criterio</span>
          <SegmentedControl
            opciones={comoOpciones(opciones.criterio_parada)}
            valor={params.criterio_parada}
            disabled={deshabilitado}
            onChange={(v: CriterioParada) => actualizar('criterio_parada', v)}
          />
        </div>

        {params.criterio_parada === 'generaciones' && (
          <Stepper
            label="Máx. generaciones"
            min={10}
            max={2000}
            paso={10}
            valor={params.max_generaciones}
            disabled={deshabilitado}
            onChange={(v) => actualizar('max_generaciones', v)}
          />
        )}

        {params.criterio_parada === 'convergencia' && (
          <div className="control-panel-fila">
            <Slider
              label="Epsilon"
              min={0}
              max={0.01}
              step={0.0001}
              valor={params.epsilon}
              disabled={deshabilitado}
              formato={(v) => v.toFixed(4)}
              onChange={(v) => actualizar('epsilon', v)}
            />
            <Stepper
              label="Paciencia"
              min={5}
              max={200}
              paso={5}
              valor={params.paciencia}
              disabled={deshabilitado}
              onChange={(v) => actualizar('paciencia', v)}
            />
          </div>
        )}

        {params.criterio_parada === 'objetivo' && (
          <Slider
            label="Aptitud objetivo"
            min={0}
            max={1}
            step={0.01}
            valor={params.aptitud_objetivo}
            disabled={deshabilitado}
            formato={FORMATO_PCT}
            onChange={(v) => actualizar('aptitud_objetivo', v)}
          />
        )}

        <ListRow
          label="Seed del AG"
          value={
            <input
              className="ui-textfield ui-textfield-compacta"
              type="number"
              value={params.seed ?? ''}
              placeholder="aleatoria"
              disabled={deshabilitado}
              onChange={(e) => {
                const v = e.target.value
                actualizar('seed', v === '' ? null : Number(v))
              }}
            />
          }
        />
      </Card>

      <div className="button-row">
        <Button onClick={onIniciar} disabled={!puedeIniciar}>
          Iniciar
        </Button>
        <Button variant="tinted" onClick={onPausar} disabled={!puedePausar}>
          Pausar
        </Button>
        <Button variant="tinted" onClick={onReanudar} disabled={!puedeReanudar}>
          Reanudar
        </Button>
        <Button variant="tinted" destructive onClick={onDetener} disabled={!puedeDetener}>
          Detener
        </Button>
      </div>
    </div>
  )
}
