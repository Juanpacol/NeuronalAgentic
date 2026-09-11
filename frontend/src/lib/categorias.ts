/**
 * Color y etiqueta por categoría del catálogo de alimentos (ver CATEGORIAS en
 * alimentos.py). Se alinean a propósito con los colores de ActivityRings
 * (carbohidratos=naranja, proteínas=verde, grasas=índigo) para que el mismo
 * macro se vea del mismo color en el genotipo y en los anillos de meta.
 * --ios-red queda afuera de este mapa: ese color está reservado para la
 * señal de "te pasaste de la meta" en ActivityRings, no para una categoría.
 */
export const COLOR_CATEGORIA: Record<string, string> = {
  carbohidratos: 'var(--ios-orange)',
  proteinas: 'var(--ios-green)',
  verduras_frutas: 'var(--cheshire-gold)',
  grasas_otros: 'var(--ios-indigo)',
}

export const CATEGORIA_ETIQUETA: Record<string, string> = {
  carbohidratos: 'Carbohidratos',
  proteinas: 'Proteínas',
  verduras_frutas: 'Verduras y frutas',
  grasas_otros: 'Grasas y otros',
}

export function colorCategoria(categoria: string): string {
  return COLOR_CATEGORIA[categoria] ?? 'var(--ios-g3)'
}
