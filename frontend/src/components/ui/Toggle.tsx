interface ToggleProps {
  on: boolean
  onChange: (on: boolean) => void
  disabled?: boolean
  /** Texto accesible cuando el interruptor va sin etiqueta visible al lado. */
  etiqueta?: string
}

/** Interruptor de iOS: 51×31 con perilla de 27px. */
export function Toggle({ on, onChange, disabled, etiqueta }: ToggleProps) {
  return (
    <span className="ui-toggle">
      <input
        className="ui-toggle-input"
        type="checkbox"
        role="switch"
        checked={on}
        disabled={disabled}
        aria-label={etiqueta}
        onChange={(e) => onChange(e.target.checked)}
      />
      <span className="ui-toggle-pista" aria-hidden="true" />
    </span>
  )
}
