import { useState } from 'react'
import { Card } from './ui/Card'
import { Stepper } from './ui/Stepper'
import { SegmentedControl, type OpcionSegmentada } from './ui/SegmentedControl'
import { Button } from './ui/Button'
import { calcularMetas, type DatosPersonales, type NivelActividad, type Sexo } from '../lib/calculadoraMetas'

interface CalculadoraMetasProps {
  disabled?: boolean
  onAplicar: (metas: {
    objetivo_kcal: number
    objetivo_proteina_g: number
    objetivo_carbohidratos_g: number
    objetivo_grasa_g: number
  }) => void
}

const OPCIONES_SEXO: OpcionSegmentada<Sexo>[] = [
  { valor: 'masculino', etiqueta: 'Hombre' },
  { valor: 'femenino', etiqueta: 'Mujer' },
]

const OPCIONES_ACTIVIDAD: OpcionSegmentada<NivelActividad>[] = [
  { valor: 'sedentario', etiqueta: 'Sedentario' },
  { valor: 'ligero', etiqueta: 'Ligero' },
  { valor: 'moderado', etiqueta: 'Moderado' },
  { valor: 'activo', etiqueta: 'Activo' },
  { valor: 'atleta', etiqueta: 'Atleta' },
]

/**
 * Para quien no sabe de entrada cuántas kcal/proteína/carbos/grasa poner:
 * a partir de sexo, edad, peso, estatura y actividad calcula el IMC (solo
 * como referencia) y el gasto energético real (Mifflin-St Jeor + factor de
 * actividad), y con un botón aplica esas metas a los sliders de arriba.
 */
export function CalculadoraMetas({ disabled, onAplicar }: CalculadoraMetasProps) {
  const [datos, setDatos] = useState<DatosPersonales>({
    sexo: 'masculino',
    edad: 30,
    peso_kg: 70,
    altura_cm: 170,
    actividad: 'moderado',
  })

  function actualizar<K extends keyof DatosPersonales>(campo: K, valor: DatosPersonales[K]) {
    setDatos({ ...datos, [campo]: valor })
  }

  const metas = calcularMetas(datos)

  return (
    <Card
      titulo="Calculadora de metas (si no sabés qué poner)"
      subtitulo="Completá tus datos y el gato calcula las metas por vos."
      footer="Estimación a partir de tu IMC y gasto energético (Mifflin-St Jeor). Ajustá los sliders de abajo después si querés afinar."
      acento="rosa"
    >
      <div className="control-panel-campo">
        <span className="ui-slider-label">Sexo</span>
        <SegmentedControl
          opciones={OPCIONES_SEXO}
          valor={datos.sexo}
          disabled={disabled}
          onChange={(v) => actualizar('sexo', v)}
        />
      </div>

      <div className="control-panel-fila">
        <Stepper
          label="Edad"
          min={14}
          max={90}
          valor={datos.edad}
          disabled={disabled}
          onChange={(v) => actualizar('edad', v)}
        />
        <Stepper
          label="Peso (kg)"
          min={30}
          max={200}
          valor={datos.peso_kg}
          disabled={disabled}
          onChange={(v) => actualizar('peso_kg', v)}
        />
        <Stepper
          label="Estatura (cm)"
          min={130}
          max={220}
          valor={datos.altura_cm}
          disabled={disabled}
          onChange={(v) => actualizar('altura_cm', v)}
        />
      </div>

      <div className="control-panel-campo">
        <span className="ui-slider-label">Nivel de actividad</span>
        <SegmentedControl
          opciones={OPCIONES_ACTIVIDAD}
          valor={datos.actividad}
          disabled={disabled}
          onChange={(v) => actualizar('actividad', v)}
        />
      </div>

      <div className="calculadora-resultado">
        <div className="calculadora-resultado-fila">
          <span>IMC</span>
          <span>
            {metas.imc.toFixed(1)} — {metas.categoriaImc}
          </span>
        </div>
        <div className="calculadora-resultado-fila">
          <span>Gasto energético estimado</span>
          <span>{Math.round(metas.get)} kcal/día</span>
        </div>
      </div>

      <Button
        variant="tinted"
        tono="rosa"
        bloque
        disabled={disabled}
        onClick={() =>
          onAplicar({
            objetivo_kcal: metas.objetivo_kcal,
            objetivo_proteina_g: metas.objetivo_proteina_g,
            objetivo_carbohidratos_g: metas.objetivo_carbohidratos_g,
            objetivo_grasa_g: metas.objetivo_grasa_g,
          })
        }
      >
        Aplicar a las metas
      </Button>
    </Card>
  )
}
