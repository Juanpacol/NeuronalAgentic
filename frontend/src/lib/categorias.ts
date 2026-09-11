/** Color por categoría del catálogo de alimentos (ver CATEGORIAS en alimentos.py). */
export const COLOR_CATEGORIA: Record<string, string> = {
  carbohidratos: 'var(--ios-orange)',
  proteinas: 'var(--ios-red)',
  verduras_frutas: 'var(--ios-green)',
  grasas_otros: 'var(--ios-indigo)',
}

export function colorCategoria(categoria: string): string {
  return COLOR_CATEGORIA[categoria] ?? 'var(--ios-g3)'
}
