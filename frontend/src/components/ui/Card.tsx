import type { ReactNode } from 'react'

interface CardProps {
  titulo?: string
  footer?: ReactNode
  children: ReactNode
  /** Sin padding interno: para tarjetas que solo contienen ListRow. */
  plano?: boolean
  className?: string
}

/** Tarjeta al estilo "inset grouped" de iOS. */
export function Card({ titulo, footer, children, plano, className }: CardProps) {
  return (
    <section className={className}>
      {titulo && <h2 className="ui-card-titulo">{titulo}</h2>}
      <div className="ui-card">
        <div className={plano ? 'ui-card-cuerpo ui-card-cuerpo-plano' : 'ui-card-cuerpo'}>
          {children}
        </div>
      </div>
      {footer && <p className="ui-card-footer">{footer}</p>}
    </section>
  )
}
