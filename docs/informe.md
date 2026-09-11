# Informe — Laboratorio de Algoritmos Genéticos

## Mapeo de componentes del curso al código

| Componente (diapositivas) | Archivo | Descripción |
|---|---|---|
| C1 — Población | `backend/app/ag/poblacion.py` | Creación de la población inicial y cálculo de estadísticas (mejor, promedio, peor) |
| C2 — Mecanismo de representación | `backend/app/ag/representacion.py` | Cromosoma lineal: array de floats normalizados, bloques de 10 genes por triángulo |
| C3 — Función objetivo | `backend/app/ag/fitness.py` | Rasterizado con Pillow + comparación de píxeles contra la imagen objetivo |
| C4 — Operadores genéticos (selección) | `backend/app/ag/seleccion.py` | Proporcional, torneo, estocástica (SUS), heurística |
| C4 — Operadores genéticos (cruce) | `backend/app/ag/cruce.py` | Un punto, dos puntos, uniforme |
| C4 — Operadores genéticos (mutación) | `backend/app/ag/mutacion.py` | Heurística (gaussiana), intercambio, desplazamiento, inserción |
| C5 — Parámetros iniciales | `backend/app/ag/parametros.py` | Tamaño de población, probabilidades, elitismo, criterio de parada |

## Sobre los operadores de mutación de permutación

Las diapositivas del curso presentan intercambio, desplazamiento e inserción como técnicas de
mutación pensadas originalmente para cromosomas donde el orden de los genes *es* la solución
(por ejemplo, una ruta o una secuencia). El cromosoma de este proyecto no es de ese tipo: es un
vector de floats donde cada bloque de 10 posiciones describe un triángulo independiente.

Aplicarlos de forma literal (intercambiar dos floats sueltos, o desplazar genes individuales)
no tendría ningún efecto con sentido semántico — mezclaría, por ejemplo, una coordenada X con
un canal de color. La adaptación implementada opera sobre **triángulos completos** (bloques de
10 genes) en vez de genes sueltos:

- **Intercambio**: cambia el orden de pintado de dos triángulos.
- **Desplazamiento**: rota un bloque de triángulos k posiciones, cambiando su profundidad relativa.
- **Inserción**: extrae un triángulo y lo reinserta en otra posición del orden de pintado.

Como el renderizado sigue el algoritmo del pintor (los triángulos se dibujan en el orden del
cromosoma, unos sobre otros), estos operadores sí tienen un efecto real: cambian qué triángulo
queda encima de cuál. Pero es importante ser honestos: cuando los triángulos no se solapan en
la imagen, el efecto en los píxeles resultantes es nulo. Por eso se presentan en la interfaz
como "operadores de reordenamiento de capas" y no como mutaciones de color o forma — el único
operador que explora genuinamente el espacio de posición y color es la mutación heurística
(perturbación gaussiana), que es la que queda como valor por defecto.

## Comparación de técnicas

(completar tras correr el laboratorio con semilla fija y registrar generación de convergencia
por cada combinación de selección/cruce/mutación)

| Selección | Cruce | Mutación | Generación de convergencia | Aptitud final |
|---|---|---|---|---|
| | | | | |
