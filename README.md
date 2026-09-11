# NeuronalAgentic — Laboratorio de Algoritmos Genéticos

Aproximación evolutiva de imágenes: una población de individuos, cada uno formado por
triángulos de color semitransparentes, evoluciona generación tras generación hasta que la
imagen renderizada se parece a una fotografía objetivo. Todas las técnicas de la asignatura
(selección, cruce, mutación, elitismo, criterios de parada) se pueden activar y comparar en
vivo desde la interfaz.

## Qué es

Proyecto para la asignatura de Algoritmos Genéticos. El backend en Python implementa el AG
siguiendo la taxonomía de las diapositivas del curso (población, mecanismo de representación,
función objetivo, operadores genéticos, parámetros iniciales) y transmite cada generación por
WebSocket; el frontend en React dibuja el resultado en un `<canvas>` y expone los controles.

## Tecnología

- **Backend**: Python 3.12, FastAPI, numpy, Pillow. Streaming por WebSocket.
- **Frontend**: React + Vite + TypeScript, Canvas 2D, uPlot para la gráfica de aptitud.
- **Infraestructura**: Docker + docker-compose para desarrollo local, GitHub Actions para
  CI/CD, Render (backend) y Vercel (frontend) para producción.

## Arquitectura

```
Frontend (Vercel)                      Backend (Render)
React + Vite + TS                      FastAPI + numpy + Pillow
  ├─ GenomeCanvas: dibuja el genoma      ├─ app/ag/  ← núcleo del AG (C1..C5)
  ├─ ControlPanel: parámetros y técnicas ├─ motor: bucle evolutivo asíncrono
  ├─ FitnessChart: aptitud por gen.      └─ ws: streaming por generación
  └─ TargetPanel: imagen objetivo
            └──────── WebSocket (genoma + estadísticas) ────────┘
```

El backend nunca envía imágenes renderizadas: envía el genoma (lista de triángulos) y el
frontend lo dibuja vectorialmente en canvas. Un genoma de 80 triángulos pesa ~5-6 KB en JSON,
frente a 80-150 KB de un PNG equivalente, y además se ve nítido a cualquier resolución.

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
| C2 — Representación | `backend/app/ag/representacion.py` | cromosoma lineal: N triángulos × 10 genes |
| C3 — Función objetivo | `backend/app/ag/fitness.py` | comparación de píxeles contra la imagen objetivo |
| C4 — Selección | `backend/app/ag/seleccion.py` | proporcional, torneo, estocástica (SUS), heurística |
| C4 — Cruce | `backend/app/ag/cruce.py` | un punto, dos puntos, uniforme |
| C4 — Mutación | `backend/app/ag/mutacion.py` | heurística (gaussiana), intercambio, desplazamiento, inserción |
| C5 — Parámetros / parada | `backend/app/ag/parametros.py`, `parada.py` | máx. generaciones, convergencia, aptitud objetivo |

Nota honesta (ver `docs/informe.md`): los operadores de intercambio, desplazamiento e
inserción son operadores de permutación pensados para cromosomas de orden. Sobre un
cromosoma de triángulos se adaptan como **operadores de reordenamiento de capas**: cambian
el orden de pintado, no la forma ni el color, y son neutros en píxeles cuando los triángulos
no se solapan.

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
VITE_WS_URL=ws://localhost:8000/ws
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

- Render free tier: 0.1 CPU compartida / 512 MB — el AG corre bastante más lento que en
  local (~4-7 generaciones/segundo en vez de decenas). Se suspende tras ~15 min de
  inactividad; el primer acceso puede tardar hasta 50s en despertar (la interfaz lo indica).
  Estado en memoria: un reinicio de la instancia pierde las corridas activas.
- Vercel Hobby: sin problema para una SPA estática, no interviene en el WebSocket.

## Créditos

Material de curso: presentación de Jorge E. Giraldo Plaza (`docs/algoritmos_geneticos.pptx`)
y notebook de referencia (`docs/Copia_de_AlgoritmoGeneticoModelo_1.ipynb`).
