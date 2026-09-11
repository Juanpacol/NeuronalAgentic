import { useEffect, useState, type RefObject } from 'react'
import type { Alimento, ObjetivosDieta } from '../lib/tipos'
import { colorCategoria } from '../lib/categorias'
import { Card } from './ui/Card'
import { ChromosomeStrip } from './viz/ChromosomeStrip'
import { ActivityRings, type AnilloMacro } from './viz/ActivityRings'
import { CheshireGrin } from './viz/CheshireGrin'

interface DietaPanelProps {
  alimentosRef: RefObject<Alimento[]>
  genomaRef: RefObject<number[] | null>
  objetivosRef: RefObject<ObjetivosDieta | null>
}

const FORMATO_COP = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 })

/**
 * La mejor dieta de la generación actual: tira de cromosoma (porciones por
 * alimento, coloreada por categoría), anillos de progreso por macro y la
 * tabla con el detalle. Se refresca a ~8Hz leyendo refs (no estado), igual
 * que el resto de la app, para no forzar re-render de React en cada
 * generación del AG.
 */
export function DietaPanel({ alimentosRef, genomaRef, objetivosRef }: DietaPanelProps) {
  const [, forzarRender] = useState(0)

  useEffect(() => {
    let frameId: number
    let ultimoGenoma: number[] | null = null

    function loop() {
      if (genomaRef.current !== ultimoGenoma) {
        ultimoGenoma = genomaRef.current
        forzarRender((n) => n + 1)
      }
      frameId = requestAnimationFrame(loop)
    }
    frameId = requestAnimationFrame(loop)

    return () => cancelAnimationFrame(frameId)
  }, [genomaRef])

  const alimentos = alimentosRef.current ?? []
  const genoma = genomaRef.current
  const objetivos = objetivosRef.current

  if (!genoma || alimentos.length === 0) {
    return (
      <Card titulo="Dieta">
        <CheshireGrin etiqueta="El gato desapareció: presioná Iniciar y va a dejar tu dieta, como la sonrisa." />
      </Card>
    )
  }

  const elegidos = alimentos
    .map((a, i) => ({ alimento: a, porciones: genoma[i] ?? 0 }))
    .filter((f) => f.porciones > 0)

  const costoTotal = elegidos.reduce((acc, f) => acc + f.alimento.precio_cop * f.porciones, 0)

  const macros = alimentos.reduce(
    (acc, a, i) => {
      const p = genoma[i] ?? 0
      acc.kcal += a.kcal * p
      acc.proteina_g += a.proteina_g * p
      acc.carbohidratos_g += a.carbohidratos_g * p
      acc.grasa_g += a.grasa_g * p
      return acc
    },
    { kcal: 0, proteina_g: 0, carbohidratos_g: 0, grasa_g: 0 },
  )

  const anillos: AnilloMacro[] = objetivos
    ? [
        { etiqueta: 'Calorías', logrado: macros.kcal, objetivo: objetivos.kcal, color: 'var(--ios-blue)', unidad: 'kcal' },
        { etiqueta: 'Proteína', logrado: macros.proteina_g, objetivo: objetivos.proteina_g, color: 'var(--ios-red)', unidad: 'g' },
        { etiqueta: 'Carbohidratos', logrado: macros.carbohidratos_g, objetivo: objetivos.carbohidratos_g, color: 'var(--ios-orange)', unidad: 'g' },
        { etiqueta: 'Grasa', logrado: macros.grasa_g, objetivo: objetivos.grasa_g, color: 'var(--ios-indigo)', unidad: 'g' },
      ]
    : []

  return (
    <div className="dieta-panel">
      <Card titulo="Genotipo — porciones por alimento">
        <ChromosomeStrip
          valores={genoma}
          maximos={alimentos.map((a) => a.max_porciones)}
          colores={alimentos.map((a) => colorCategoria(a.categoria))}
          nombres={alimentos.map((a) => a.nombre)}
        />
      </Card>

      {objetivos && (
        <Card titulo="Macros vs. meta">
          <ActivityRings anillos={anillos} />
        </Card>
      )}

      <Card
        titulo="Detalle de la dieta"
        footer={
          <>
            Costo total: {FORMATO_COP.format(costoTotal)}
            {objetivos ? ` / presupuesto ${FORMATO_COP.format(objetivos.presupuesto_cop)}` : ''}
          </>
        }
      >
        <div className="dieta-tabla-wrap">
          <table className="dieta-tabla">
            <thead>
              <tr>
                <th>Alimento</th>
                <th>Porciones</th>
                <th>kcal</th>
                <th>Proteína (g)</th>
                <th>Carbs (g)</th>
                <th>Grasa (g)</th>
                <th>Costo</th>
              </tr>
            </thead>
            <tbody>
              {elegidos.map((f) => (
                <tr key={f.alimento.codigo_tcac}>
                  <td>{f.alimento.nombre}</td>
                  <td>
                    {f.porciones} {f.alimento.unidad}
                    {f.porciones > 1 ? 's' : ''}
                  </td>
                  <td>{(f.alimento.kcal * f.porciones).toFixed(0)}</td>
                  <td>{(f.alimento.proteina_g * f.porciones).toFixed(1)}</td>
                  <td>{(f.alimento.carbohidratos_g * f.porciones).toFixed(1)}</td>
                  <td>{(f.alimento.grasa_g * f.porciones).toFixed(1)}</td>
                  <td>{FORMATO_COP.format(f.alimento.precio_cop * f.porciones)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
