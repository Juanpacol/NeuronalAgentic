import { useEffect, useState, type RefObject } from 'react'
import type { Alimento, ObjetivosDieta } from '../lib/tipos'

interface DietaPanelProps {
  alimentosRef: RefObject<Alimento[]>
  genomaRef: RefObject<number[] | null>
  objetivosRef: RefObject<ObjetivosDieta | null>
}

const FORMATO_COP = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 })

/**
 * Tabla de la mejor dieta de la generación actual: porciones elegidas por
 * alimento y costo. Se refresca a ~8Hz vía requestAnimationFrame leyendo
 * refs (no estado), igual que el antiguo RouteCanvas, para no forzar
 * re-render de React en cada generación del AG.
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
      <div className="dieta-panel dieta-panel-vacio">
        <p>Aún no hay una dieta generada. Presiona Iniciar.</p>
      </div>
    )
  }

  const elegidos = alimentos
    .map((a, i) => ({ alimento: a, porciones: genoma[i] ?? 0 }))
    .filter((f) => f.porciones > 0)

  const costoTotal = elegidos.reduce((acc, f) => acc + f.alimento.precio_cop * f.porciones, 0)

  return (
    <div className="dieta-panel">
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
      <p className="dieta-costo-total">
        Costo total: {FORMATO_COP.format(costoTotal)}
        {objetivos ? ` / presupuesto ${FORMATO_COP.format(objetivos.presupuesto_cop)}` : ''}
      </p>
    </div>
  )
}
