import type { ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  onClick?: () => void
  variant?: 'filled' | 'tinted' | 'plain'
  destructive?: boolean
  disabled?: boolean
  /** Ocupa todo el ancho disponible. */
  bloque?: boolean
  type?: 'button' | 'submit'
}

/**
 * Botón de iOS. Las clases .boton/.boton-filled/.boton-tinted/.boton-plain ya
 * existen en errores.css (la tarjeta de error depende de ellas); aquí se
 * reutilizan tal cual y solo se añaden los modificadores nuevos.
 */
export function Button({
  children,
  onClick,
  variant = 'filled',
  destructive,
  disabled,
  bloque,
  type = 'button',
}: ButtonProps) {
  const clases = ['boton', `boton-${variant}`]
  if (destructive) clases.push('boton-destructive')
  if (bloque) clases.push('boton-bloque')

  return (
    <button type={type} className={clases.join(' ')} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  )
}
