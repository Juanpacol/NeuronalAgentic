'use client'

import { useEffect, useRef, type ComponentPropsWithoutRef } from 'react'
import { useInView, useMotionValue, useSpring } from 'motion/react'

import { cn } from '../../lib/utils'

interface NumberTickerProps extends ComponentPropsWithoutRef<'span'> {
  value: number
  startValue?: number
  direction?: 'up' | 'down'
  delay?: number
  decimalPlaces?: number
  locale?: string
}

/** Cifra que hace spring hacia el valor objetivo; usada en los StatTile del AG. */
export function NumberTicker({
  value,
  startValue = 0,
  direction = 'up',
  delay = 0,
  className,
  decimalPlaces = 0,
  locale = 'es-CO',
  ...props
}: NumberTickerProps) {
  const ref = useRef<HTMLSpanElement>(null)
  const motionValue = useMotionValue(direction === 'down' ? value : startValue)
  const springValue = useSpring(motionValue, {
    damping: 30,
    stiffness: 90,
  })
  const isInView = useInView(ref, { once: true, margin: '0px' })

  // A diferencia del ejemplo original (que solo anima una vez al entrar en
  // viewport), aquí el valor cambia en vivo con cada generación del AG: cada
  // cambio de `value` reanima el spring hacia el nuevo objetivo.
  useEffect(() => {
    if (!isInView) return
    const timer = setTimeout(() => {
      motionValue.set(value)
    }, delay * 1000)
    return () => clearTimeout(timer)
  }, [motionValue, isInView, delay, value])

  useEffect(
    () =>
      springValue.on('change', (latest) => {
        if (ref.current) {
          ref.current.textContent = new Intl.NumberFormat(locale, {
            minimumFractionDigits: decimalPlaces,
            maximumFractionDigits: decimalPlaces,
          }).format(Number(latest.toFixed(decimalPlaces)))
        }
      }),
    [springValue, decimalPlaces, locale],
  )

  return (
    <span ref={ref} className={cn('ui-numberticker', className)} {...props}>
      {startValue}
    </span>
  )
}
