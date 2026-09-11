interface CheshireGrinProps {
  /** Texto opcional debajo de la sonrisa (p. ej. "Despertando al gato…"). */
  etiqueta?: string
  /** Ancho del SVG. Por defecto 140px (uso en cards); pasar uno chico para uso inline (p. ej. junto al título). */
  tamano?: number
  className?: string
}

/**
 * Guiño a "The Cheshire Diet": solo ojos y sonrisa. A propósito NO es el
 * reskin completo de Wonderland que se evaluó — mismo fondo negro y tokens
 * iOS de siempre, con dos acentos puntuales (--cheshire-gold/--cheshire-pink)
 * solo acá.
 */
export function CheshireGrin({ etiqueta, tamano = 140, className }: CheshireGrinProps) {
  return (
    <div
      className={className ? `cheshire-grin ${className}` : 'cheshire-grin'}
      role="img"
      aria-label={etiqueta ?? 'El gato de Cheshire'}
    >
      <svg
        viewBox="0 0 200 120"
        className="cheshire-grin-svg"
        style={{ width: tamano }}
        aria-hidden="true"
      >
        <ellipse cx="70" cy="40" rx="11" ry="14" className="cheshire-grin-ojo" />
        <ellipse cx="130" cy="40" rx="11" ry="14" className="cheshire-grin-ojo" />
        <circle cx="70" cy="40" r="4.5" className="cheshire-grin-pupila" />
        <circle cx="130" cy="40" r="4.5" className="cheshire-grin-pupila" />
        <path
          d="M45 62 Q100 100 155 62"
          className="cheshire-grin-sonrisa"
          fill="none"
          strokeLinecap="round"
        />
        <path d="M62 68 L68 78 L74 68 Z" className="cheshire-grin-diente" />
        <path d="M92 76 L98 86 L104 76 Z" className="cheshire-grin-diente" />
        <path d="M126 68 L132 78 L138 68 Z" className="cheshire-grin-diente" />
      </svg>
      {etiqueta && <p className="cheshire-grin-etiqueta">{etiqueta}</p>}
    </div>
  )
}
