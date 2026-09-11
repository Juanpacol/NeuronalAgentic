import { clsx, type ClassValue } from 'clsx'

/** Concatena classNames, ignorando falsy/undefined. */
export function cn(...inputs: ClassValue[]): string {
  return clsx(inputs)
}
