#!/usr/bin/env python3
"""Demo standalone (sin FastAPI): corre el AG de TSP contra un mapa de ciudades
generado con semilla fija e imprime cómo baja la distancia por generación.

Uso: python scripts/demo_local.py   (ejecutado desde backend/)
"""
from __future__ import annotations

import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ag.ciudades import calcular_matriz_distancias, generar_ciudades
from app.ag.motor import evolucionar
from app.ag.parametros import ParametrosAG

MAX_GENERACIONES = int(os.environ.get("DEMO_GENERACIONES", "400"))


async def main():
    params = ParametrosAG(
        poblacion=60,
        num_ciudades=30,
        max_generaciones=MAX_GENERACIONES,
        criterio_parada="generaciones",
        seed=42,
        semilla_ciudades=1,
    )

    ciudades = generar_ciudades(params.num_ciudades, params.semilla_ciudades)
    matriz = calcular_matriz_distancias(ciudades)

    print(f"Corriendo AG TSP: poblacion={params.poblacion}, ciudades={params.num_ciudades}, "
          f"generaciones={params.max_generaciones}, seleccion={params.seleccion}, "
          f"cruce={params.cruce}, mutacion={params.mutacion}")

    inicio = time.perf_counter()
    ruta_final = None
    async for estado in evolucionar(params, matriz):
        ruta_final = estado.ruta_mejor
        if estado.generacion % 40 == 0 or estado.razon_parada:
            print(
                f"gen={estado.generacion:4d}  distancia_mejor={estado.distancia_mejor:.4f}  "
                f"distancia_promedio={estado.distancia_promedio:.4f}  "
                f"sin_mejora={estado.generaciones_sin_mejora}"
            )
        if estado.razon_parada:
            print(f"Parada: {estado.razon_parada}")

    duracion = time.perf_counter() - inicio
    print(f"Tiempo total: {duracion:.1f}s")
    print(f"Ruta final: {[int(x) for x in ruta_final]}")


if __name__ == "__main__":
    asyncio.run(main())
