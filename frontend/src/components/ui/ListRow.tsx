import type { ReactNode } from 'react'

interface ListRowProps {
  label: ReactNode
  value?: ReactNode
  accessory?: ReactNode
  onClick?: () => void
}

/** Fila de lista agrupada: alto mínimo 44px y separador con sangría. */
export function ListRow({ label, value, accessory, onClick }: ListRowProps) {
  const contenido = (
    <>
      <span className="ui-listrow-label">{label}</span>
      {value !== undefined && <span className="ui-listrow-value">{value}</span>}
      {accessory && <span className="ui-listrow-accessory">{accessory}</span>}
    </>
  )

  if (onClick) {
    return (
      <button type="button" className="ui-listrow ui-listrow-clicable" onClick={onClick}>
        {contenido}
      </button>
    )
  }

  return <div className="ui-listrow">{contenido}</div>
}
