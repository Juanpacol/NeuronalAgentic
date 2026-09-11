import { useEffect, useState } from 'react'
import { Button } from './Button'
import { Card } from './Card'
import { ListRow } from './ListRow'
import { SegmentedControl } from './SegmentedControl'
import { Slider } from './Slider'
import { StatTile } from './StatTile'
import { Stepper } from './Stepper'
import { Toggle } from './Toggle'
import { ActivityRings } from '../viz/ActivityRings'
import { ChromosomeStrip } from '../viz/ChromosomeStrip'
import { GenerationCounter } from '../viz/GenerationCounter'
import { PopulationGrid } from '../viz/PopulationGrid'

const SELECCIONES = [
  { valor: 'proporcional', etiqueta: 'Proporcional' },
  { valor: 'torneo', etiqueta: 'Torneo' },
  { valor: 'estocastica', etiqueta: 'Estocástica' },
  { valor: 'heuristica', etiqueta: 'Heurística' },
] as const

const CRUCES = [
  { valor: 'un_punto', etiqueta: '1 punto' },
  { valor: 'dos_puntos', etiqueta: '2 puntos' },
  { valor: 'uniforme', etiqueta: 'Uniforme' },
] as const

const CATEGORIAS = ['var(--ios-blue)', 'var(--ios-green)', 'var(--ios-orange)', 'var(--ios-indigo)']

const N_GENES = 25
const N_INDIVIDUOS = 80

/**
 * Vista de muestra de todo el sistema de diseño, con datos simulados.
 * No depende del backend. Se abre con ?showcase=1 y es de usar y tirar:
 * cuando la Fase 5 conecte los componentes al dominio real, se puede borrar.
 */
export function Showcase() {
  const [seleccion, setSeleccion] = useState<(typeof SELECCIONES)[number]['valor']>('torneo')
  const [cruce, setCruce] = useState<(typeof CRUCES)[number]['valor']>('dos_puntos')
  const [probCruce, setProbCruce] = useState(0.85)
  const [poblacion, setPoblacion] = useState(80)
  const [elitismo, setElitismo] = useState(3)
  const [avanzado, setAvanzado] = useState(false)
  const [tick, setTick] = useState(0)

  // Simula el flujo de generaciones a ~8Hz, igual que el volcado real, para
  // comprobar que las transiciones de 140ms no se encolan ni tiemblan.
  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 120)
    return () => clearInterval(id)
  }, [])

  const progreso = Math.min(1, tick / 200)
  const generacion = Math.min(400, tick * 2)

  const valores = Array.from({ length: N_GENES }, (_, i) => {
    const base = Math.abs(Math.sin(i * 1.7 + tick * 0.03))
    return Math.round(base * 4 * progreso)
  })
  const maximos = Array.from({ length: N_GENES }, (_, i) => (i % 3 === 0 ? 3 : 4))
  const colores = Array.from({ length: N_GENES }, (_, i) => CATEGORIAS[i % CATEGORIAS.length])

  const aptitudes = Array.from({ length: N_INDIVIDUOS }, (_, i) => {
    const rango = 1 - i / N_INDIVIDUOS
    return 0.2 + rango * 0.6 * progreso + 0.1 * progreso
  })

  return (
    <div className="showcase">
      <h1 className="showcase-titulo">Sistema de diseño</h1>
      <p className="showcase-sub">
        Datos simulados a ~8&nbsp;Hz para verificar animación y modo oscuro.
      </p>

      <div className="showcase-columnas">
        <div className="showcase-col">
          <Card titulo="Anillos de macros">
            <ActivityRings
              anillos={[
                {
                  etiqueta: 'Calorías',
                  logrado: 1200 + progreso * 1400,
                  objetivo: 2000,
                  color: 'var(--ios-red)',
                  unidad: 'kcal',
                },
                {
                  etiqueta: 'Proteína',
                  logrado: 30 + progreso * 50,
                  objetivo: 75,
                  color: 'var(--ios-green)',
                  unidad: 'g',
                },
                {
                  etiqueta: 'Carbohidratos',
                  logrado: 90 + progreso * 150,
                  objetivo: 250,
                  color: 'var(--ios-blue)',
                  unidad: 'g',
                },
                {
                  etiqueta: 'Grasa',
                  logrado: 20 + progreso * 40,
                  objetivo: 65,
                  color: 'var(--ios-orange)',
                  unidad: 'g',
                },
              ]}
            />
            <ChromosomeStrip valores={valores} maximos={maximos} colores={colores} />
            <div className="viz-cromosoma-pie">
              <span>Genotipo del mejor individuo</span>
              <span>{N_GENES} genes</span>
            </div>
          </Card>

          <Card titulo="Población">
            <PopulationGrid aptitudes={aptitudes} />
          </Card>

          <Card titulo="Estadísticas">
            <div className="showcase-stats">
              <GenerationCounter generacion={generacion} maxGeneraciones={400} />
              <StatTile label="Mejor aptitud" valor={(0.4 + progreso * 0.5).toFixed(4)} tono="verde" />
              <StatTile label="Costo" valor={Math.round(24000 - progreso * 6000)} unidad="COP" tono="azul" />
              <StatTile label="Desviación" valor={`${Math.round(60 - progreso * 52)}%`} tono="naranja" />
            </div>
          </Card>

          <Card titulo="Dieta seleccionada" plano>
            <ListRow label="Arroz blanco" value="2 porciones · 410 kcal" />
            <ListRow label="Huevo" value="3 porciones · 210 kcal" />
            <ListRow label="Frijol cargamanto" value="1 porción · 240 kcal" />
            <ListRow label="Aguacate" value="1 porción · 160 kcal" />
          </Card>
        </div>

        <div className="showcase-col showcase-col-ajustes">
          <Card titulo="Operadores">
            <div className="showcase-campo">
              <span className="ui-slider-label">Selección</span>
              <SegmentedControl
                opciones={SELECCIONES}
                valor={seleccion}
                onChange={setSeleccion}
                etiquetaGrupo="Técnica de selección"
              />
            </div>
            <div className="showcase-campo">
              <span className="ui-slider-label">Cruce</span>
              <SegmentedControl
                opciones={CRUCES}
                valor={cruce}
                onChange={setCruce}
                etiquetaGrupo="Técnica de cruce"
              />
            </div>
            <div className="showcase-campo">
              <Slider
                label="Prob. de cruce"
                min={0}
                max={1}
                step={0.01}
                valor={probCruce}
                onChange={setProbCruce}
                formato={(v) => v.toFixed(2)}
              />
            </div>
          </Card>

          <Card titulo="Parámetros" plano>
            <div className="ui-listrow">
              <Stepper label="Población" min={10} max={200} paso={10} valor={poblacion} onChange={setPoblacion} />
            </div>
            <div className="ui-listrow">
              <Stepper label="Elitismo" min={0} max={10} valor={elitismo} onChange={setElitismo} />
            </div>
            <ListRow
              label="Modo avanzado"
              accessory={<Toggle on={avanzado} onChange={setAvanzado} etiqueta="Modo avanzado" />}
            />
          </Card>

          <Card titulo="Acciones">
            <div className="showcase-botones">
              <Button variant="filled">Iniciar</Button>
              <Button variant="tinted">Pausar</Button>
              <Button variant="plain">Reanudar</Button>
              <Button variant="filled" destructive>
                Detener
              </Button>
              <Button variant="filled" disabled>
                Deshabilitado
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
