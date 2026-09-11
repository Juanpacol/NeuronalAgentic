import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'
import type { Alimento, ObjetivosDieta } from './tipos'
import { calcularResumenDieta } from './dietaResumen'
import { CATEGORIA_ETIQUETA } from './categorias'

interface GenerarPdfDietaArgs {
  alimentos: Alimento[]
  genoma: number[]
  objetivos: ObjetivosDieta | null
  /** Canvas de la gráfica de aptitud (FitnessChart), si ya está montada. */
  canvasGrafica: HTMLCanvasElement | null
}

const FORMATO_COP = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 })
// RGB de --cheshire-gold, para el encabezado de la tabla.
const ORO_RGB: [number, number, number] = [246, 211, 131]

/** Genera y descarga un PDF con el plan de alimentación completo y la gráfica de aptitud. */
export function generarPdfDieta({ alimentos, genoma, objetivos, canvasGrafica }: GenerarPdfDietaArgs): void {
  const { elegidos, macros, costoTotal } = calcularResumenDieta(alimentos, genoma)
  const doc = new jsPDF()
  const anchoPagina = doc.internal.pageSize.getWidth()

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(20)
  doc.text('The Cheshire Diet', 14, 18)
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  doc.setTextColor(120)
  doc.text(`Generado el ${new Date().toLocaleString('es-CO')}`, 14, 24)
  doc.setTextColor(0)

  let y = 32

  if (objetivos) {
    doc.setFontSize(11)
    doc.text('Metas nutricionales — logrado / meta', 14, y)
    y += 6
    doc.setFontSize(9)
    const lineas = [
      `Calorías: ${macros.kcal.toFixed(0)} / ${objetivos.kcal} kcal`,
      `Proteína: ${macros.proteina_g.toFixed(1)} / ${objetivos.proteina_g} g`,
      `Carbohidratos: ${macros.carbohidratos_g.toFixed(1)} / ${objetivos.carbohidratos_g} g`,
      `Grasa: ${macros.grasa_g.toFixed(1)} / ${objetivos.grasa_g} g`,
      `Costo: ${FORMATO_COP.format(costoTotal)} / presupuesto ${FORMATO_COP.format(objetivos.presupuesto_cop)}`,
    ]
    for (const linea of lineas) {
      doc.text(linea, 14, y)
      y += 5
    }
    y += 4
  }

  autoTable(doc, {
    startY: y,
    head: [['Alimento', 'Categoría', 'Porciones', 'kcal', 'Proteína (g)', 'Carbs (g)', 'Grasa (g)', 'Costo']],
    body: elegidos.map((f) => [
      f.alimento.nombre,
      CATEGORIA_ETIQUETA[f.alimento.categoria] ?? f.alimento.categoria,
      `${f.porciones} ${f.alimento.unidad}${f.porciones > 1 ? 's' : ''}`,
      (f.alimento.kcal * f.porciones).toFixed(0),
      (f.alimento.proteina_g * f.porciones).toFixed(1),
      (f.alimento.carbohidratos_g * f.porciones).toFixed(1),
      (f.alimento.grasa_g * f.porciones).toFixed(1),
      FORMATO_COP.format(f.alimento.precio_cop * f.porciones),
    ]),
    styles: { fontSize: 8 },
    headStyles: { fillColor: ORO_RGB, textColor: [30, 20, 0] },
    margin: { left: 14, right: 14 },
  })

  // jspdf-autotable no tipa `lastAutoTable` en el documento (lo agrega en
  // runtime al aplicar el plugin); se lee con un cast puntual.
  const finalY = (doc as unknown as { lastAutoTable?: { finalY: number } }).lastAutoTable?.finalY ?? y

  doc.setFontSize(9)
  doc.text(
    `Costo total: ${FORMATO_COP.format(costoTotal)}${objetivos ? ` / presupuesto ${FORMATO_COP.format(objetivos.presupuesto_cop)}` : ''}`,
    14,
    finalY + 6,
  )

  if (canvasGrafica) {
    const altoPagina = doc.internal.pageSize.getHeight()
    const anchoImg = anchoPagina - 28
    const altoImg = anchoImg * (canvasGrafica.height / canvasGrafica.width)
    let yGrafica = finalY + 14

    if (yGrafica + altoImg + 10 > altoPagina) {
      doc.addPage()
      yGrafica = 18
    }

    doc.setFontSize(11)
    doc.text('Evolución de la aptitud', 14, yGrafica)
    yGrafica += 4

    // Fondo blanco: el canvas de la app es transparente (pensado para el
    // fondo negro de la UI) y se vería mal flotando sobre una página blanca.
    doc.setFillColor(255, 255, 255)
    doc.rect(14, yGrafica, anchoImg, altoImg, 'F')
    doc.addImage(canvasGrafica.toDataURL('image/png'), 'PNG', 14, yGrafica, anchoImg, altoImg)
  }

  doc.save('the-cheshire-diet.pdf')
}
