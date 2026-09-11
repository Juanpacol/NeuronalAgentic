import { Card } from './ui/Card'

interface DocumentacionProps {
  onCerrar: () => void
}

/**
 * "Cómo funciona": explica el AG de dieta mapeado a la taxonomía del curso
 * (C1-C5), en el mismo lenguaje simple que pide el profesor. Contenido fijo
 * (no depende del backend) porque describe el diseño, no una corrida — se
 * mantiene a mano en este archivo junto con el código que describe.
 */
export function Documentacion({ onCerrar }: DocumentacionProps) {
  return (
    <div className="doc-backdrop" onClick={onCerrar}>
      <div className="doc-modal" onClick={(e) => e.stopPropagation()}>
        <div className="doc-cabecera">
          <h2>Cómo funciona</h2>
          <button type="button" className="sidebar-cerrar" onClick={onCerrar} aria-label="Cerrar documentación">
            ✕
          </button>
        </div>

        <div className="doc-cuerpo">
          <p className="doc-intro">
            Este laboratorio optimiza un plan de alimentación diario con un algoritmo genético
            (AG): una población de dietas candidatas evoluciona generación tras generación hasta
            acercarse lo más posible a tus metas nutricionales, al menor costo. Abajo está cada
            pieza del AG que pide la asignatura, mapeada al archivo real que la implementa.
          </p>

          <Card titulo="C1 — Población" acento="verde">
            <p>
              Un individuo es una dieta candidata completa. La población es un conjunto de N
              dietas (parámetro "Población" en los ajustes) que se evalúan y evolucionan juntas
              cada generación. <code>poblacion.py</code> crea la población inicial y calcula sus
              estadísticas (mejor, promedio, peor aptitud) en cada paso.
            </p>
          </Card>

          <Card titulo="C2 — Representación del cromosoma" acento="azul">
            <p>
              El cromosoma es un vector de enteros: un gen por alimento del catálogo (25
              alimentos), y el valor del gen son las porciones diarias de ese alimento. 0
              significa "no está en la dieta". No hay un gen de máscara aparte — sería
              información redundante (máscara=0 con cantidad=7 describiría lo mismo que
              máscara=1 con cantidad=0). Cada gen tiene su propia cota (
              <code>max_porciones</code>), no una cota global: 4 tazas de arroz es razonable, 4
              aguacates no. <code>representacion.py</code>.
            </p>
          </Card>

          <Card titulo="C3 — Función objetivo" acento="naranja">
            <p>
              Aptitud = <code>1 / (1 + penalización)</code>, en (0, 1]; mayor es mejor. La
              penalización suma dos partes: qué tan lejos está la dieta de las 4 metas
              nutricionales (kcal, proteína, carbohidratos, grasa — error relativo ponderado) y
              qué tan cara es respecto al presupuesto (término proporcional + recargo si se
              excede). El parámetro "Peso del costo vs. nutrición" controla cuánto pesa el costo
              frente a la nutrición. <code>fitness.py</code>, catálogo en{' '}
              <code>alimentos.py</code>.
            </p>
          </Card>

          <Card titulo="C4 — Selección de padres" acento="rosa">
            <p>
              Cuatro técnicas, todas favoreciendo mayor aptitud: <strong>proporcional</strong>{' '}
              (ruleta, probabilidad proporcional a la aptitud), <strong>torneo</strong> (se
              eligen k individuos al azar y gana el de mayor aptitud), <strong>estocástica</strong>{' '}
              (muestreo universal estocástico — como la ruleta pero con muestras equiespaciadas,
              menos ruido), y <strong>heurística</strong> (truncamiento: solo los N mejores
              pueden ser padres). <code>seleccion.py</code>.
            </p>
          </Card>

          <Card titulo="C4 — Cruce" acento="verde">
            <p>
              Un punto, dos puntos y uniforme — los tres tal como se enseñan, sin adaptación.
              Esto es más simple que en el proyecto anterior (TSP): ahí el cromosoma era una
              permutación de ciudades y cortar/pegar segmentos producía rutas inválidas (ciudades
              repetidas), así que hacía falta Order Crossover con reparación. Acá cada gen es
              independiente y ya viene acotado (<code>[0, max_porciones[i]]</code>), así que
              cualquier combinación posicional de dos padres válidos también es válida — no hace
              falta reparar nada. <code>cruce.py</code>.
            </p>
          </Card>

          <Card titulo="C4 — Mutación" acento="azul">
            <p>
              De los 4 operadores que pide el curso, solo 2 tienen sentido pleno sobre un vector
              de cantidades — el resto se incluyen por completitud del requisito, no porque
              rindan mejor:
            </p>
            <ul className="doc-lista">
              <li>
                <strong>Heurística</strong> — sentido pleno: perturbación gaussiana por gen
                (búsqueda local alrededor del individuo actual).
              </li>
              <li>
                <strong>Intercambio</strong> — sentido dentro de categoría: intercambiar arroz
                por arepa (ambos carbohidratos) es sustituir un básico por otro comparable;
                intercambiar arroz por pollo no tendría sentido nutricional, así que el operador
                se restringe a la misma categoría.
              </li>
              <li>
                <strong>Desplazamiento</strong> e <strong>inserción</strong> — operadores de
                permutación: presuponen que la posición del gen significa algo. Acá la posición
                es solo el orden del alimento en el catálogo, sin contenido real, así que el
                movimiento es casi arbitrario. Se espera que rindan peor — eso es un resultado
                del experimento, no un error.
              </li>
            </ul>
            <p>
              <code>mutacion.py</code>.
            </p>
          </Card>

          <Card titulo="C5 — Parámetros iniciales y parada" acento="naranja">
            <p>
              Tamaño de población, probabilidades de cruce/mutación, elitismo (cuántos de los
              mejores pasan directo a la siguiente generación sin cruzarse) y semilla opcional
              para reproducibilidad. Tres criterios de parada: <strong>máx. generaciones</strong>{' '}
              (corta a un número fijo), <strong>convergencia</strong> (para si pasan N
              generaciones sin mejorar la mejor aptitud) y <strong>objetivo</strong> (para al
              alcanzar una aptitud mínima). <code>parametros.py</code>, <code>parada.py</code>.
            </p>
          </Card>

          <Card titulo="Por qué dieta y no otro problema" acento="rosa">
            <p>
              La primera versión aproximaba una fotografía con triángulos evolucionados. Se
              abandonó porque necesitaba decenas de miles de generaciones para un resultado
              reconocible, y casi ninguna implementación de referencia usa un AG poblacional
              real con cruce (la mayoría son hill-climbing: mutar una copia y quedarse con la
              mejor), lo que no permite comparar selección/cruce/mutación como pide la
              asignatura. Dieta resuelve esto: el fitness se calcula en microsegundos, converge
              en decenas de generaciones, y los 4 operadores de mutación tienen una
              interpretación real sobre un vector de cantidades.
            </p>
          </Card>
        </div>
      </div>
    </div>
  )
}
