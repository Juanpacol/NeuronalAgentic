interface StepperProps {
  label: string
  min: number
  max: number
  paso?: number
  valor: number
  onChange: (valor: number) => void
  disabled?: boolean
}

/** Stepper de iOS: fila con etiqueta, valor y la pastilla de −/+. */
export function Stepper({
  label,
  min,
  max,
  paso = 1,
  valor,
  onChange,
  disabled,
}: StepperProps) {
  const ajustar = (delta: number) => {
    const siguiente = Math.min(max, Math.max(min, valor + delta))
    if (siguiente !== valor) onChange(siguiente)
  }

  return (
    <div className="ui-stepper-campo">
      <span className="ui-listrow-label">{label}</span>
      <span className="ui-stepper-valor">{valor}</span>
      <span className="ui-stepper">
        <button
          type="button"
          className="ui-stepper-boton"
          onClick={() => ajustar(-paso)}
          disabled={disabled || valor <= min}
          aria-label={`Disminuir ${label}`}
        >
          −
        </button>
        <span className="ui-stepper-divisor" aria-hidden="true" />
        <button
          type="button"
          className="ui-stepper-boton"
          onClick={() => ajustar(paso)}
          disabled={disabled || valor >= max}
          aria-label={`Aumentar ${label}`}
        >
          +
        </button>
      </span>
    </div>
  )
}
