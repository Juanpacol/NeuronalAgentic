import type { Alimento, MacrosDieta } from './tipos'

export interface FilaDieta {
  alimento: Alimento
  porciones: number
}

export interface ResumenDieta {
  elegidos: FilaDieta[]
  macros: MacrosDieta
  costoTotal: number
}

/** Deriva la lista de alimentos elegidos, macros totales y costo total del genoma actual. */
export function calcularResumenDieta(alimentos: Alimento[], genoma: number[]): ResumenDieta {
  const elegidos = alimentos
    .map((a, i) => ({ alimento: a, porciones: genoma[i] ?? 0 }))
    .filter((f) => f.porciones > 0)

  const costoTotal = elegidos.reduce((acc, f) => acc + f.alimento.precio_cop * f.porciones, 0)

  const macros = alimentos.reduce(
    (acc, a, i) => {
      const p = genoma[i] ?? 0
      acc.kcal += a.kcal * p
      acc.proteina_g += a.proteina_g * p
      acc.carbohidratos_g += a.carbohidratos_g * p
      acc.grasa_g += a.grasa_g * p
      return acc
    },
    { kcal: 0, proteina_g: 0, carbohidratos_g: 0, grasa_g: 0 },
  )

  return { elegidos, macros, costoTotal }
}
