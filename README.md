# NeuronalAgentic — Laboratorio de Algoritmos Genéticos (TSP)

Problema del vendedor viajero (TSP): una población de rutas evoluciona generación tras
generación hasta encontrar el recorrido más corto que visita todas las ciudades una vez y
vuelve al origen. Todas las técnicas de la asignatura (selección, cruce, mutación, elitismo,
criterios de parada) se pueden activar y comparar en vivo desde la interfaz, con convergencia
real en cientos de generaciones (segundos, no minutos u horas).

## Qué es

Proyecto para la asignatura de Algoritmos Genéticos. El backend en Python implementa el AG
siguiendo la taxonomía de las diapositivas del curso (población, mecanismo de representación,
función objetivo, operadores genéticos, parámetros iniciales) y transmite cada generación por
WebSocket; el frontend en React dibuja las ciudades y la mejor ruta en un `<canvas>` y expone
los controles.

## Por qué TSP (y no aproximación de imágenes)

La primera versión de este proyecto intentaba aproximar una fotografía con triángulos de color
evolucionados. Se abandonó tras confirmar (con referencias reales como EvoLisa/genetic-lisa,
polygen, image-approx) que ese enfoque necesita decenas o cientos de miles de generaciones para
un resultado reconocible, y que casi ninguna de esas implementaciones usa un AG poblacional con
cruce real — la mayoría son hill-climbing (mutar una copia, quedarse con el mejor), lo que
contradice el objetivo de la asignatura de comparar técnicas de selección/cruce/mutación. TSP
resuelve esto: el fitness se calcula en microsegundos (suma de distancias), converge en cientos
de generaciones, y los 4 operadores de mutación del curso (heurística, intercambio,
desplazamiento, inserción) tienen sentido **literal** sobre una permutación de ciudades — a
diferencia de los triángulos, donde 3 de los 4 solo reordenaban capas de pintado.

## Tecnología

- **Backend**: Python 3.12, FastAPI, numpy. Streaming por WebSocket.
- **Frontend**: React + Vite + TypeScript, Canvas 2D, uPlot para la gráfica de distancia.
- **Infraestructura**: Docker + docker-compose para desarrollo local, GitHub Actions para
  CI/CD, Render (backend) y Vercel (frontend) para producción.

## Arquitectura

```
Frontend (Vercel)                      Backend (Render)
React + Vite + TS                      FastAPI + numpy
  ├─ RouteCanvas: ciudades + ruta        ├─ app/ag/  ← núcleo del AG (C1..C5)
  ├─ ControlPanel: parámetros y técnicas ├─ motor: bucle evolutivo asíncrono
  └─ FitnessChart: distancia por gen.    └─ ws: streaming por generación
            └──────── WebSocket (ciudades + ruta + estadísticas) ────────┘
```

El backend genera el mapa de ciudades al iniciar una corrida y lo envía una sola vez (mensaje
`iniciado`); luego, por cada generación, envía solo estadísticas de distancia y — cuando el
mejor individuo mejoró — la ruta (permutación de índices de ciudad). El frontend dibuja las
ciudades y conecta la ruta con líneas directamente en canvas, sin depender de imágenes.

## Cómo correr

### Con Docker (recomendado — un solo comando)

```bash
docker compose up
```

Backend en `http://localhost:8000`, frontend en `http://localhost:5173`. Si esos puertos ya
están ocupados por otro proyecto, cambia el mapeo sin tocar el archivo:

```bash
BACKEND_PORT=8091 FRONTEND_PORT=5174 docker compose up
```

### Sin Docker (manual — dos terminales)

```bash
# Terminal 1 — backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Parámetros y técnicas del AG

| Componente (diapositivas) | Archivo | Técnicas implementadas |
|---|---|---|
| C1 — Población | `backend/app/ag/poblacion.py` | creación y estadísticas de la población |
| C2 — Representación | `backend/app/ag/representacion.py` | cromosoma = permutación de ciudades |
| C3 — Función objetivo | `backend/app/ag/fitness.py`, `ciudades.py` | distancia total de la ruta (ciclo cerrado) |
| C4 — Selección | `backend/app/ag/seleccion.py` | proporcional, torneo, estocástica (SUS), heurística |
| C4 — Cruce | `backend/app/ag/cruce.py` | un punto, dos puntos, uniforme (variantes de Order Crossover — OX) |
| C4 — Mutación | `backend/app/ag/mutacion.py` | heurística (2-opt simplificado), intercambio, desplazamiento, inserción |
| C5 — Parámetros / parada | `backend/app/ag/parametros.py`, `parada.py` | máx. generaciones, convergencia, distancia objetivo |

A diferencia de un AG binario/real genérico, en TSP el cromosoma es una **permutación**: el
cruce no puede cortar y pegar genes sueltos (produciría rutas con ciudades repetidas o
faltantes). Por eso `un_punto`/`dos_puntos`/`uniforme` están implementados como variantes de
**Order Crossover (OX)**, que reparan automáticamente los duplicados — mismo nombre que pide el
curso, adaptación estándar de la literatura para representaciones de permutación (ver
`docs/informe.md`).

## Variables de entorno

`backend/.env.example`:
```
PORT=8000
ALLOWED_ORIGINS=http://localhost:5173
MAX_RUNS_CONCURRENTES=2
```

`frontend/.env.example`:
```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws/evolucion
```

## Despliegue

- **Backend → Render**: Web Service desde este repo, `rootDir: backend`, runtime Docker
  (usa `render.yaml`). Auto-deploy solo cuando los checks de GitHub Actions pasan
  (`autoDeployTrigger: checksPass`). Configurar `ALLOWED_ORIGINS` con el dominio de Vercel.
- **Frontend → Vercel**: importar el repo, Root Directory `frontend`, framework Vite
  (usa `frontend/vercel.json`). Configurar `VITE_API_URL` y `VITE_WS_URL` (con `wss://`)
  apuntando al backend de Render.
- **CI/CD**: cada push/PR corre lint + tests + build (`.github/workflows/ci.yml`); cada
  merge a `main` publica ambas imágenes Docker en GHCR (`docker-publish.yml`); un cron cada
  10 min mantiene despierto el backend gratuito de Render (`keep-alive.yml`).

## Limitaciones del plan gratuito

- Render free tier: 0.1 CPU compartida / 512 MB. A diferencia del enfoque de imagen anterior,
  el fitness de TSP es tan barato (suma de distancias) que esto deja de ser un cuello de
  botella real — cientos de generaciones corren en segundos incluso con CPU compartida.
  Se suspende tras ~15 min de inactividad; el primer acceso puede tardar hasta 50s en despertar
  (la interfaz lo indica). Estado en memoria: un reinicio de la instancia pierde las corridas
  activas.
- Vercel Hobby: sin problema para una SPA estática, no interviene en el WebSocket.

## Créditos

Material de curso: presentación de Jorge E. Giraldo Plaza (`docs/algoritmos_geneticos.pptx`)
y notebook de referencia (`docs/Copia_de_AlgoritmoGeneticoModelo_1.ipynb`).
