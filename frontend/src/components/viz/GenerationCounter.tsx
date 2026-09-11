interface GenerationCounterProps {
  generacion: number
  maxGeneraciones: number
}

const RADIO = 44
const CIRCUNFERENCIA = 2 * Math.PI * RADIO

/** Contador de generación con anillo de progreso, al estilo de un marcador de vueltas. */
export function GenerationCounter({ generacion, maxGeneraciones }: GenerationCounterProps) {
  const p = maxGeneraciones > 0 ? Math.min(1, generacion / maxGeneraciones) : 0
  const offset = CIRCUNFERENCIA * (1 - p)

  return (
    <div className="viz-generacion">
      <svg className="viz-generacion-svg" viewBox="0 0 96 96" aria-hidden="true">
        <g transform="rotate(-90 48 48)">
          <circle
            className="viz-generacion-pista"
            cx="48"
            cy="48"
            r={RADIO}
            fill="none"
            stroke="var(--ios-blue)"
            strokeWidth="4"
          />
          <circle
            className="viz-generacion-arco"
            cx="48"
            cy="48"
            r={RADIO}
            fill="none"
            stroke="var(--ios-blue)"
            strokeWidth="4"
            strokeLinecap="round"
            strokeDasharray={CIRCUNFERENCIA}
            strokeDashoffset={offset}
          />
        </g>
      </svg>
      <span className="viz-generacion-cifra">{generacion}</span>
      <span className="viz-generacion-label">de {maxGeneraciones}</span>
    </div>
  )
}
