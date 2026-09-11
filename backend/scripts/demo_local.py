#!/usr/bin/env python3
"""Demo standalone (sin FastAPI): corre el motor contra frontend/public/target.jpg
y guarda el PNG del mejor individuo final.

Uso: python scripts/demo_local.py   (ejecutado desde backend/)
"""
from __future__ import annotations

import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

from app.ag.fitness import preparar_objetivo, rasterizar
from app.ag.motor import evolucionar
from app.ag.parametros import ParametrosAG

RUTA_TARGET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "frontend", "public", "target.jpg",
)
RUTA_SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultado_demo.png")

MAX_GENERACIONES = int(os.environ.get("DEMO_GENERACIONES", "200"))


async def main():
    params = ParametrosAG(
        poblacion=40,
        num_triangulos=80,
        max_generaciones=MAX_GENERACIONES,
        criterio_parada="generaciones",
        resolucion_trabajo=128,
        seed=42,
    )

    imagen = Image.open(RUTA_TARGET)
    objetivo = preparar_objetivo(imagen, params.resolucion_trabajo)

    print(f"Corriendo AG: poblacion={params.poblacion}, triangulos={params.num_triangulos}, "
          f"generaciones={params.max_generaciones}, resolucion={params.resolucion_trabajo}")

    inicio = time.perf_counter()
    genoma_final = None
    async for estado in evolucionar(params, objetivo):
        genoma_final = estado.genoma_mejor
        if estado.generacion % 20 == 0 or estado.razon_parada:
            print(
                f"gen={estado.generacion:4d}  mejor={estado.mejor_aptitud:.4f}  "
                f"promedio={estado.aptitud_promedio:.4f}  peor={estado.aptitud_peor:.4f}  "
                f"sin_mejora={estado.generaciones_sin_mejora}"
            )
        if estado.razon_parada:
            print(f"Parada: {estado.razon_parada}")

    duracion = time.perf_counter() - inicio
    print(f"Tiempo total: {duracion:.1f}s")

    render_final = rasterizar(genoma_final, params.resolucion_trabajo).convert("RGB")
    render_final.save(RUTA_SALIDA)
    print(f"Resultado guardado en {RUTA_SALIDA}")


if __name__ == "__main__":
    asyncio.run(main())
