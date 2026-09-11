export type TonoStat = 'neutro' | 'azul' | 'verde' | 'rojo' | 'naranja'

interface StatTileProps {
  label: string
  valor: string | number
  unidad?: string
  tono?: TonoStat
  /** Destella en verde 200ms; se usa al encontrar un nuevo mejor individuo. */
  destello?: boolean
}

/** Cifra grande con etiqueta. Siempre tabular-nums: si no, el número baila al fluir. */
export function StatTile({ label, valor, unidad, tono = 'neutro', destello }: StatTileProps) {
  const clases = ['ui-stattile']
  if (tono !== 'neutro') clases.push(`ui-stattile-${tono}`)
  if (destello) clases.push('ui-stattile-destello')

  return (
    <div className={clases.join(' ')}>
      <div className="ui-stattile-valor">
        {valor}
        {unidad && <span className="ui-stattile-unidad">{unidad}</span>}
      </div>
      <div className="ui-stattile-label">{label}</div>
    </div>
  )
}
