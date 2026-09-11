export interface AnilloMacro {
  etiqueta: string
  logrado: number
  objetivo: number
  /** Color CSS del anillo; usa tokens (var(--ios-red), etc.). */
  color: string
  unidad?: string
}

interface ActivityRingsProps {
  anillos: AnilloMacro[]
}

/** Radios de los cuatro anillos concéntricos, de fuera hacia dentro. */
const RADIOS = [86, 68, 50, 32]
const GROSOR = 16
/** Umbral a partir del cual se considera exceso (5% por encima de la meta). */
const UMBRAL_EXCESO = 1.05

function redondear(n: number): string {
  return Math.round(n).toLocaleString('es-CO')
}

/**
 * Anillos concéntricos de progreso por macronutriente.
 *
 * A diferencia de las apps de actividad, aquí el sobrepaso NO se envuelve:
 * pasarse de calorías es un fallo, no un logro. El arco se fija en 100% y el
 * anillo avisa en rojo con un pulso, mostrando cuánto se excedió.
 */
export function ActivityRings({ anillos }: ActivityRingsProps) {
  return (
    <div className="viz-anillos">
      <svg className="viz-anillos-svg" viewBox="0 0 200 200" role="img" aria-label="Progreso por macronutriente">
        <g transform="rotate(-90 100 100)">
          {anillos.slice(0, RADIOS.length).map((anillo, i) => {
            const r = RADIOS[i]
            const circunferencia = 2 * Math.PI * r
            const p = anillo.objetivo > 0 ? anillo.logrado / anillo.objetivo : 0
            const excedido = p > UMBRAL_EXCESO
            const offset = circunferencia * (1 - Math.min(p, 1))
            const color = excedido ? 'var(--ios-red)' : anillo.color

            return (
              <g key={anillo.etiqueta}>
                <circle
                  className="viz-anillo-pista"
                  cx="100"
                  cy="100"
                  r={r}
                  fill="none"
                  stroke={color}
                  strokeWidth={GROSOR}
                />
                <circle
                  className={excedido ? 'viz-anillo-arco viz-anillo-exceso' : 'viz-anillo-arco'}
                  cx="100"
                  cy="100"
                  r={r}
                  fill="none"
                  stroke={color}
                  strokeWidth={GROSOR}
                  strokeLinecap="round"
                  strokeDasharray={circunferencia}
                  strokeDashoffset={offset}
                />
              </g>
            )
          })}
        </g>
      </svg>

      <div className="viz-anillos-leyenda">
        {anillos.map((anillo) => {
          const p = anillo.objetivo > 0 ? anillo.logrado / anillo.objetivo : 0
          const excedido = p > UMBRAL_EXCESO
          const exceso = anillo.logrado - anillo.objetivo
          return (
            <div className="viz-anillos-item" key={anillo.etiqueta}>
              <span
                className="viz-anillos-punto"
                style={{ background: excedido ? 'var(--ios-red)' : anillo.color }}
              />
              <span className="viz-anillos-etiqueta">{anillo.etiqueta}</span>
              <span className="viz-anillos-cifra">
                {redondear(anillo.logrado)} / {redondear(anillo.objetivo)}
                {anillo.unidad ? ` ${anillo.unidad}` : ''}
              </span>
              {excedido && (
                <span className="viz-anillos-exceso">
                  +{redondear(exceso)}
                  {anillo.unidad ? ` ${anillo.unidad}` : ''}
                </span>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
