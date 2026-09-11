import type { CSSProperties } from 'react'

interface PopulationGridProps {
  /** Aptitud de cada individuo (el motor ya las envía ordenadas). */
  aptitudes: number[]
  columnas?: number
}

/**
 * Rejilla de la población: una celda por individuo, teñida según su aptitud.
 *
 * Más allá de lo decorativo, hace visible la convergencia prematura: si toda
 * la rejilla se vuelve del mismo verde de golpe, la población perdió
 * diversidad y el AG dejó de explorar.
 */
export function PopulationGrid({ aptitudes, columnas = 10 }: PopulationGridProps) {
  const min = aptitudes.length > 0 ? Math.min(...aptitudes) : 0
  const max = aptitudes.length > 0 ? Math.max(...aptitudes) : 1
  const rango = max - min

  const estiloRejilla = { '--cols': columnas } as CSSProperties

  return (
    <div>
      <div
        className="viz-poblacion"
        style={estiloRejilla}
        role="img"
        aria-label={`Aptitud de ${aptitudes.length} individuos`}
      >
        {aptitudes.map((aptitud, i) => {
          const t = rango > 0 ? (aptitud - min) / rango : 1
          const pct = 8 + t * 92
          return (
            <div
              key={i}
              className="viz-poblacion-celda"
              style={{ background: `color-mix(in srgb, var(--ios-green) ${pct}%, var(--bg-3))` }}
              title={aptitud.toFixed(4)}
            />
          )
        })}
      </div>
      <div className="viz-poblacion-pie">
        <span>peor</span>
        <span className="viz-poblacion-escala" aria-hidden="true" />
        <span>mejor</span>
      </div>
    </div>
  )
}
