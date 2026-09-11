# Informe — Laboratorio de Algoritmos Genéticos (Dieta)

> Nota: este proyecto pivoteó de TSP (vendedor viajero) a optimización de dieta. La versión
> anterior de este informe describía TSP; se reemplaza por completo acá. La misma explicación,
> en lenguaje simple, también vive dentro de la app (botón "Cómo funciona").

## Qué optimiza

Una población de dietas candidatas evoluciona generación tras generación hacia la mejor
combinación de alimentos que cumpla metas nutricionales (kcal, proteína, carbohidratos, grasa)
al menor costo posible, dado un catálogo real de 25 alimentos con datos de la Tabla de
Composición de Alimentos Colombianos (TCAC, ICBF/UNAL 2018).

## Mapeo de componentes del curso al código

| Componente (diapositivas) | Archivo | Descripción |
|---|---|---|
| C1 — Población | `backend/app/ag/poblacion.py` | Creación de la población inicial y estadísticas (mejor/promedio/peor aptitud) por generación |
| C2 — Representación | `backend/app/ag/representacion.py` | Cromosoma = vector de enteros; `genoma[i]` = porciones diarias del alimento `i` (0 = no incluido). Cota por gen (`max_porciones[i]`), no global |
| C3 — Función objetivo | `backend/app/ag/fitness.py`, catálogo en `alimentos.py` | `aptitud = 1/(1+penalización)`; penalización = desviación ponderada de metas nutricionales + penalización de costo (proporcional + recargo si excede presupuesto) |
| C4 — Selección | `backend/app/ag/seleccion.py` | Proporcional (ruleta), torneo, estocástica (SUS), heurística (truncamiento) |
| C4 — Cruce | `backend/app/ag/cruce.py` | Un punto, dos puntos, uniforme — tal como se enseñan, sin adaptación (ver más abajo) |
| C4 — Mutación | `backend/app/ag/mutacion.py` | Heurística (perturbación gaussiana), intercambio (dentro de categoría), desplazamiento, inserción |
| C5 — Parámetros / parada | `backend/app/ag/parametros.py`, `parada.py` | Población, probabilidades, elitismo, semilla; criterios: máx. generaciones, convergencia (paciencia), objetivo de aptitud |

## Por qué el cruce NO necesita reparación acá (a diferencia de TSP)

En TSP el cromosoma era una permutación de ciudades: cortar y pegar segmentos de dos padres casi
siempre producía una ruta inválida (ciudades repetidas o faltantes), por lo que hacía falta Order
Crossover (OX) con reparación para garantizar una permutación válida.

En el dominio de dieta cada gen es una cantidad independiente, ya acotada individualmente
(`[0, max_porciones[i]]`). Cualquier combinación posicional de genes de dos padres válidos
también respeta esas cotas, porque cada gen conserva su posición y, con ella, su cota. Por eso
`un_punto`, `dos_puntos` y `uniforme` son los operadores de manual sin ninguna adaptación —
una simplificación real frente al proyecto anterior, no una casualidad.

## Honestidad sobre los 4 operadores de mutación

Solo 2 de los 4 operadores que pide el curso tienen sentido pleno sobre un vector de cantidades:

- **Heurística** — sentido pleno: perturbación gaussiana por gen, proporcional a la cota de ese
  alimento. Es la mutación natural de este dominio.
- **Intercambio** — sentido dentro de categoría: intercambiar arroz por arepa (ambos
  carbohidratos) es sustituir un básico por otro comparable; intercambiar arroz por pollo no
  tiene sentido nutricional, así que el operador se restringe a alimentos de la misma categoría.
- **Desplazamiento** e **inserción** — operadores de permutación: presuponen que la posición del
  gen significa algo. Acá la posición es solo el orden del alimento en el catálogo, sin
  contenido real, así que el movimiento es casi arbitrario. Se incluyen por completitud frente
  al requisito de la asignatura, y se espera que rindan peor — eso es un resultado del
  experimento a documentar, no un defecto de la implementación.

## Por qué dieta y no aproximación de imágenes (el proyecto original)

La primera versión evolucionaba triángulos de color para aproximar una fotografía. Se abandonó
tras confirmar contra implementaciones reales de referencia (EvoLisa/genetic-lisa, image-approx,
polygen) que ese enfoque necesita decenas o cientos de miles de generaciones para un resultado
reconocible, y que la mayoría de esas implementaciones son hill-climbing (mutar una copia,
quedarse con la mejor) y no un AG poblacional con cruce real — lo que no permite comparar
selección/cruce/mutación como pide la asignatura. Dieta resuelve esto: el fitness se calcula en
microsegundos, converge en decenas de generaciones, y los 4 operadores de mutación tienen una
interpretación real sobre esta representación.

## Rendimiento medido

Con los parámetros por defecto (población 80, torneo k=3, cruce de dos puntos, mutación
heurística): converge a aptitud ~0.88 alrededor de la generación 40 (ver
`backend/scripts/demo_local.py`), con desviación de macros por debajo de 1% y costo bien por
debajo del presupuesto. Por eso el default de `max_generaciones` es 80, no varios cientos: correr
mucho más allá de la convergencia solo agrega generaciones planas sin más búsqueda útil.

## Comparación de técnicas

(completar tras correr el laboratorio con semilla fija y registrar generación de convergencia
por cada combinación de selección/cruce/mutación)

| Selección | Cruce | Mutación | Generación de convergencia | Aptitud final |
|---|---|---|---|---|
| | | | | |
