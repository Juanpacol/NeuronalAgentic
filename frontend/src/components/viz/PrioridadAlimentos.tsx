export interface FilaPrioridad {
  id: string
  nombre: string
  categoria: string
  valor: number
  /** Texto ya formateado a mostrar junto a la barra (p. ej. "620 kcal · 2 tazas"). */
  detalle: string
  color: string
}

interface PrioridadAlimentosProps {
  filas: FilaPrioridad[]
}

/**
 * Ranking en barras horizontales: qué alimentos de la dieta aportan más de lo
 * que se está midiendo (por defecto, kcal). La barra más larga es el mayor
 * aporte, normalizada contra ese máximo (no contra el total) para que el
 * alimento top siempre se vea al 100% y el resto se compare contra él.
 */
export function PrioridadAlimentos({ filas }: PrioridadAlimentosProps) {
  if (filas.length === 0) return null

  const maximo = Math.max(...filas.map((f) => f.valor))

  return (
    <div className="viz-prioridad" role="img" aria-label="Ranking de alimentos por aporte calórico">
      {filas.map((f) => {
        const pct = maximo > 0 ? (f.valor / maximo) * 100 : 0
        return (
          <div className="viz-prioridad-fila" key={f.id}>
            <span className="viz-prioridad-nombre" title={f.nombre}>
              {f.nombre}
            </span>
            <span className="viz-prioridad-pista">
              <span
                className="viz-prioridad-barra"
                style={{ width: `${pct}%`, background: f.color }}
              />
            </span>
            <span className="viz-prioridad-detalle">{f.detalle}</span>
          </div>
        )
      })}
    </div>
  )
}
