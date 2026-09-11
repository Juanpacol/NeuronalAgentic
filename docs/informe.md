# Informe — Laboratorio de Algoritmos Genéticos (TSP)

## De la aproximación de imágenes a TSP: por qué se cambió

La primera versión del proyecto evolucionaba triángulos de color semitransparentes para
aproximar una fotografía. Se abandonó por dos razones, confirmadas contra implementaciones
reales de referencia (EvoLisa/genetic-lisa de Roger Johansson, image-approx, polygen):

1. **Escala de convergencia incompatible con un curso**: esos proyectos necesitan entre 50.000
   y 680.000+ generaciones para una foto reconocible (documentado en sus propios README). Con
   un AG poblacional real (no hill-climbing) y recursos de CPU compartida (Render free tier),
   eso es inviable para una demo en clase.
2. **La mayoría no son AG poblacionales**: son hill-climbing (un individuo, mutar una copia,
   quedarse con la que mejora). Eso no permite comparar selección/cruce/mutación como pide la
   asignatura — adoptar ese enfoque habría sido más rápido pero pedagógicamente vacío.

TSP (problema del vendedor viajero) resuelve ambos problemas: el fitness es una suma de
distancias (microsegundos, no un rasterizado de imagen), converge en cientos de generaciones, y
mantiene un AG poblacional genuino con cruce real entre individuos.

## Mapeo de componentes del curso al código

| Componente (diapositivas) | Archivo | Descripción |
|---|---|---|
| C1 — Población | `backend/app/ag/poblacion.py` | Creación de la población inicial (permutaciones aleatorias) y estadísticas |
| C2 — Mecanismo de representación | `backend/app/ag/representacion.py` | Cromosoma = permutación de `[0, num_ciudades)` |
| C3 — Función objetivo | `backend/app/ag/fitness.py`, `ciudades.py` | Distancia total de la ruta (ciclo cerrado); aptitud = 1/(1+distancia) |
| C4 — Operadores genéticos (selección) | `backend/app/ag/seleccion.py` | Proporcional, torneo, estocástica (SUS), heurística |
| C4 — Operadores genéticos (cruce) | `backend/app/ag/cruce.py` | Un punto, dos puntos, uniforme — todas variantes de Order Crossover (OX) |
| C4 — Operadores genéticos (mutación) | `backend/app/ag/mutacion.py` | Heurística (2-opt simplificado), intercambio, desplazamiento, inserción |
| C5 — Parámetros iniciales | `backend/app/ag/parametros.py` | Tamaño de población, probabilidades, elitismo, criterio de parada |

## Por qué el cruce no puede ser "de un punto" literal en TSP

Un cromosoma de permutación no admite el cruce de un punto/dos puntos/uniforme tal como se
enseña para cromosomas binarios o reales: cortar y pegar segmentos de dos padres casi siempre
produce un hijo con ciudades repetidas y otras ausentes (no es una permutación válida).

La adaptación estándar de la literatura es **Order Crossover (OX)**: se conserva un segmento de
un padre tal cual, y el resto de las ciudades se completa en el orden en que aparecen en el
otro padre, saltando las que ya están. Esto garantiza que el hijo sea siempre una permutación
válida. Se mantienen los tres nombres que pide el curso porque son variantes reales de OX:

- **un_punto**: un solo punto de corte; se conserva `p1[:c]` y se completa con el orden de `p2`.
- **dos_puntos**: OX clásico de dos puntos de corte (el segmento intermedio se conserva).
- **uniforme**: Uniform Order Crossover (UOX) — una máscara aleatoria decide qué posiciones se
  heredan directamente de un padre; el resto se completa en el orden del otro padre.

## Por qué los operadores de mutación aquí sí son literales (a diferencia de la versión de imagen)

En la versión anterior (triángulos), intercambio/desplazamiento/inserción eran operadores de
permutación aplicados por necesidad sobre un cromosoma que no era una permutación real (una
lista de triángulos con genes de color/posición), así que solo tenía sentido reinterpretarlos
como "reordenar el orden de pintado" — con efecto nulo en píxeles cuando las figuras no se
solapaban.

En TSP el cromosoma **es** una permutación, así que estos operadores aplican tal como se
enseñan, sin adaptación forzada:

- **Intercambio (swap)**: intercambia dos ciudades de posición en la ruta.
- **Desplazamiento**: toma un segmento contiguo de ciudades y lo mueve a otra posición de la ruta.
- **Inserción**: extrae una ciudad y la reinserta en otra posición.
- **Heurística**: en vez de una mutación puramente aleatoria, prueba varios intercambios
  candidatos y se queda con el que más reduce la distancia total (una forma simplificada de
  búsqueda local tipo 2-opt), aprovechando información del problema — de ahí el nombre
  "heurística".

## Rendimiento medido

Con población 60, 30 ciudades: la distancia baja de ~12.8 a ~4.8 (mejora de ~62%) en 400
generaciones, con convergencia visible desde la generación ~80 y **menos de 1 segundo** de
tiempo total en CPU local. Esto es órdenes de magnitud más rápido que el enfoque de imagen
(39 segundos para 800 generaciones con resultados visualmente pobres), y viable en el CPU
compartida del plan gratuito de Render sin comprometer la experiencia de la demo en clase.

## Comparación de técnicas

(completar tras correr el laboratorio con semilla fija y registrar generación de convergencia
por cada combinación de selección/cruce/mutación)

| Selección | Cruce | Mutación | Generación de convergencia | Distancia final |
|---|---|---|---|---|
| | | | | |
