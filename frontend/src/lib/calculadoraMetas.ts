// Calculadora de metas nutricionales a partir de datos personales, para el
// usuario que no sabe de entrada cuántas kcal/proteína/carbos/grasa poner.
//
// El IMC por sí solo (peso/estatura²) NO alcanza para fijar un objetivo
// calórico: es un índice de clasificación (bajo peso/normal/sobrepeso/
// obesidad), no de gasto energético. Por eso el cálculo real usa
// Mifflin-St Jeor (TMB) + un factor de actividad (GET), que es el estándar
// de la literatura de nutrición; el IMC se muestra aparte, como referencia.

export type Sexo = 'masculino' | 'femenino'
export type NivelActividad = 'sedentario' | 'ligero' | 'moderado' | 'activo' | 'atleta'

export interface DatosPersonales {
  sexo: Sexo
  edad: number
  peso_kg: number
  altura_cm: number
  actividad: NivelActividad
}

export interface MetasCalculadas {
  imc: number
  categoriaImc: string
  tmb: number
  get: number
  objetivo_kcal: number
  objetivo_proteina_g: number
  objetivo_carbohidratos_g: number
  objetivo_grasa_g: number
}

const FACTOR_ACTIVIDAD: Record<NivelActividad, number> = {
  sedentario: 1.2,
  ligero: 1.375,
  moderado: 1.55,
  activo: 1.725,
  atleta: 1.9,
}

/** Gramos de proteína por kg de peso corporal (rango general recomendado: 1.2–2.0). */
const PROTEINA_G_POR_KG = 1.6
/** Fracción de las kcal totales que se asignan a grasa; el resto va a carbohidratos. */
const FRACCION_KCAL_GRASA = 0.28

export function calcularImc(peso_kg: number, altura_cm: number): number {
  const altura_m = altura_cm / 100
  return peso_kg / (altura_m * altura_m)
}

export function categorizarImc(imc: number): string {
  if (imc < 18.5) return 'Bajo peso'
  if (imc < 25) return 'Normal'
  if (imc < 30) return 'Sobrepeso'
  return 'Obesidad'
}

/** Tasa metabólica basal (Mifflin-St Jeor), la fórmula con mejor precisión validada hoy. */
export function calcularTmb({ sexo, edad, peso_kg, altura_cm }: DatosPersonales): number {
  const base = 10 * peso_kg + 6.25 * altura_cm - 5 * edad
  return sexo === 'masculino' ? base + 5 : base - 161
}

export function calcularMetas(datos: DatosPersonales): MetasCalculadas {
  const imc = calcularImc(datos.peso_kg, datos.altura_cm)
  const tmb = calcularTmb(datos)
  const get = tmb * FACTOR_ACTIVIDAD[datos.actividad]

  const objetivo_proteina_g = Math.round(PROTEINA_G_POR_KG * datos.peso_kg)
  const kcal_grasa = get * FRACCION_KCAL_GRASA
  const objetivo_grasa_g = Math.round(kcal_grasa / 9)
  const kcal_proteina = objetivo_proteina_g * 4
  const kcal_carbohidratos = Math.max(0, get - kcal_grasa - kcal_proteina)
  const objetivo_carbohidratos_g = Math.round(kcal_carbohidratos / 4)

  return {
    imc,
    categoriaImc: categorizarImc(imc),
    tmb,
    get,
    objetivo_kcal: Math.round(get),
    objetivo_proteina_g,
    objetivo_carbohidratos_g,
    objetivo_grasa_g,
  }
}
