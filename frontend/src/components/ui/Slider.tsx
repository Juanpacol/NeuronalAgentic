import type { CSSProperties } from 'react'

interface SliderProps {
  label: string
  min: number
  max: number
  step?: number
  valor: number
  onChange: (valor: number) => void
  disabled?: boolean
  /** Cómo mostrar el valor junto a la etiqueta. Por defecto, el número crudo. */
  formato?: (valor: number) => string
}

/** Slider de iOS: pista fina, pulgar blanco grande y relleno azul a la izquierda. */
export function Slider({
  label,
  min,
  max,
  step = 1,
  valor,
  onChange,
  disabled,
  formato,
}: SliderProps) {
  const rango = max - min
  const pct = rango === 0 ? 0 : (valor - min) / rango
  const estilo = { '--pct': pct } as CSSProperties

  return (
    <label className="ui-slider">
      <span className="ui-slider-cabecera">
        <span className="ui-slider-label">{label}</span>
        <span className="ui-slider-valor">{formato ? formato(valor) : valor}</span>
      </span>
      <span className="ui-slider-pista">
        <input
          className="ui-slider-input"
          type="range"
          min={min}
          max={max}
          step={step}
          value={valor}
          disabled={disabled}
          style={estilo}
          onChange={(e) => onChange(e.target.valueAsNumber)}
        />
      </span>
    </label>
  )
}
