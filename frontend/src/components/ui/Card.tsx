import type { CSSProperties, ReactNode } from 'react'

export type AcentoCard = 'azul' | 'verde' | 'naranja' | 'rojo' | 'rosa'

const VAR_ACENTO: Record<AcentoCard, string> = {
  azul: 'var(--ios-blue)',
  verde: 'var(--ios-green)',
  naranja: 'var(--ios-orange)',
  rojo: 'var(--ios-red)',
  rosa: 'var(--cheshire-pink)',
}

interface CardProps {
  titulo?: string
  /** Línea corta debajo del título: qué es esta sección / qué llenar acá. */
  subtitulo?: ReactNode
  footer?: ReactNode
  children: ReactNode
  /** Sin padding interno: para tarjetas que solo contienen ListRow. */
  plano?: boolean
  className?: string
  /**
   * Tiñe los controles interactivos de esta tarjeta (sliders, foco de
   * segmented control) con un color distinto al azul por defecto, para
   * diferenciar secciones de un vistazo. Solo sobreescribe --ios-blue
   * dentro de esta tarjeta, nada global.
   */
  acento?: AcentoCard
}

/** Tarjeta al estilo "inset grouped" de iOS. */
export function Card({ titulo, subtitulo, footer, children, plano, className, acento }: CardProps) {
  const estilo = acento ? ({ '--ios-blue': VAR_ACENTO[acento] } as CSSProperties) : undefined

  return (
    <section className={className}>
      {titulo && <h2 className="ui-card-titulo">{titulo}</h2>}
      {subtitulo && <p className="ui-card-subtitulo">{subtitulo}</p>}
      <div className="ui-card" style={estilo}>
        <div className={plano ? 'ui-card-cuerpo ui-card-cuerpo-plano' : 'ui-card-cuerpo'}>
          {children}
        </div>
      </div>
      {footer && <p className="ui-card-footer">{footer}</p>}
    </section>
  )
}
