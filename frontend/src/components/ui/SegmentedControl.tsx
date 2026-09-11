import type { CSSProperties, KeyboardEvent } from 'react'

export interface OpcionSegmentada<T extends string> {
  valor: T
  etiqueta: string
}

interface SegmentedControlProps<T extends string> {
  opciones: readonly OpcionSegmentada<T>[]
  valor: T
  onChange: (valor: T) => void
  disabled?: boolean
  /** Texto accesible del grupo (no se pinta). */
  etiquetaGrupo?: string
}

/**
 * Control segmentado de iOS: la pastilla se desplaza con translateX en vez de
 * re-pintar fondos, que es lo que da la sensación de deslizamiento.
 */
export function SegmentedControl<T extends string>({
  opciones,
  valor,
  onChange,
  disabled,
  etiquetaGrupo,
}: SegmentedControlProps<T>) {
  const indice = Math.max(
    0,
    opciones.findIndex((o) => o.valor === valor),
  )

  function moverFoco(e: KeyboardEvent<HTMLDivElement>) {
    if (disabled) return
    const delta = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0
    if (delta === 0) return
    e.preventDefault()
    const siguiente = (indice + delta + opciones.length) % opciones.length
    onChange(opciones[siguiente].valor)
  }

  const estilo = { '--n': opciones.length, '--i': indice } as CSSProperties

  return (
    <div
      className="ui-segmented"
      role="radiogroup"
      aria-label={etiquetaGrupo}
      aria-disabled={disabled || undefined}
      style={estilo}
      onKeyDown={moverFoco}
    >
      <span className="ui-segmented-thumb" aria-hidden="true" />
      {opciones.map((opcion) => {
        const activa = opcion.valor === valor
        return (
          <button
            key={opcion.valor}
            type="button"
            role="radio"
            aria-checked={activa}
            tabIndex={activa ? 0 : -1}
            className="ui-segmented-opcion"
            disabled={disabled}
            onClick={() => onChange(opcion.valor)}
          >
            {opcion.etiqueta}
          </button>
        )
      })}
    </div>
  )
}
