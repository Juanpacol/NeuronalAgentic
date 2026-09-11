import type { CSSProperties } from 'react'

interface ChromosomeStripProps {
  /** Valor actual de cada gen. */
  valores: number[]
  /** Cota superior de cada gen, para normalizar la altura. */
  maximos: number[]
  /** Color por gen (normalmente derivado de su categoría). */
  colores?: string[]
  /** Nombres por gen, para el tooltip nativo. */
  nombres?: string[]
}

/**
 * Tira del cromosoma: una celda por gen, altura proporcional a su valor.
 *
 * Es literalmente el genotipo del mejor individuo. Se ve asentarse conforme
 * la corrida converge, y es lo que hace que la interfaz esté ambientada al
 * algoritmo genético y no sea solo un panel de resultados.
 */
export function ChromosomeStrip({ valores, maximos, colores, nombres }: ChromosomeStripProps) {
  return (
    <div className="viz-cromosoma" role="img" aria-label="Genotipo del mejor individuo">
      {valores.map((valor, i) => {
        const max = maximos[i] ?? 1
        const fraccion = max > 0 ? Math.min(1, Math.max(0, valor / max)) : 0
        const vacia = valor <= 0
        const estilo = {
          height: `${fraccion * 100}%`,
          '--celda-color': colores?.[i],
        } as CSSProperties

        return (
          <div
            key={i}
            className={vacia ? 'viz-cromosoma-celda viz-cromosoma-vacia' : 'viz-cromosoma-celda'}
            style={estilo}
            title={nombres?.[i] ? `${nombres[i]}: ${valor}` : String(valor)}
          />
        )
      })}
    </div>
  )
}
