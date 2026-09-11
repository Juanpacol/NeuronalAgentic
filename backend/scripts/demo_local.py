#!/usr/bin/env python3
"""Demo standalone (sin FastAPI): corre el AG de dieta e imprime la dieta final.

Uso: python scripts/demo_local.py   (ejecutado desde backend/)
"""
from __future__ import annotations

import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ag.alimentos import contexto_desde_parametros  # noqa: E402
from app.ag.fitness import resumen_dieta  # noqa: E402
from app.ag.motor import evolucionar  # noqa: E402
from app.ag.parametros import ParametrosAG  # noqa: E402

MAX_GENERACIONES = int(os.environ.get("DEMO_GENERACIONES", "400"))


async def main():
    params = ParametrosAG(
        max_generaciones=MAX_GENERACIONES,
        criterio_parada="generaciones",
        seed=42,
    )
    ctx = contexto_desde_parametros(params)

    print(
        f"AG dieta: poblacion={params.poblacion}, alimentos={ctx.num_alimentos}, "
        f"generaciones={params.max_generaciones}\n"
        f"seleccion={params.seleccion}, cruce={params.cruce}, mutacion={params.mutacion}\n"
        f"metas: {params.objetivo_kcal:.0f} kcal, {params.objetivo_proteina_g:.0f} g prot, "
        f"{params.objetivo_carbohidratos_g:.0f} g carb, {params.objetivo_grasa_g:.0f} g grasa, "
        f"presupuesto ${params.presupuesto_cop:,.0f}\n"
    )
    print(f"{'gen':>5} {'aptitud':>9} {'penaliz.':>9} {'pen_macro':>10} {'pen_costo':>10} {'costo':>9}")

    inicio = time.perf_counter()
    ultimo = None
    async for estado in evolucionar(params, ctx):
        ultimo = estado
        if estado.generacion % 40 == 0 or estado.razon_parada:
            penalizacion = 1.0 / estado.mejor_aptitud - 1.0
            print(
                f"{estado.generacion:>5} {estado.mejor_aptitud:>9.4f} {penalizacion:>9.4f} "
                f"{estado.pen_macro_mejor:>10.4f} {estado.pen_costo_mejor:>10.4f} "
                f"{estado.costo_mejor:>9,.0f}"
            )
    duracion = time.perf_counter() - inicio

    print(f"\nParada: {ultimo.razon_parada}   Tiempo: {duracion:.2f}s")

    r = resumen_dieta(ultimo.genoma_mejor, ctx)
    print("\n--- Dieta encontrada ---")
    for p in sorted(r["porciones"], key=lambda x: -x["porciones"]):
        print(f"  {p['porciones']} x {p['nombre']}")

    m = r["macros"]
    print(
        f"\n  kcal        {m['kcal']:>8.0f}  (meta {params.objetivo_kcal:.0f})\n"
        f"  proteína    {m['proteina_g']:>8.1f} g (meta {params.objetivo_proteina_g:.0f})\n"
        f"  carbohidr.  {m['carbohidratos_g']:>8.1f} g (meta {params.objetivo_carbohidratos_g:.0f})\n"
        f"  grasa       {m['grasa_g']:>8.1f} g (meta {params.objetivo_grasa_g:.0f})\n"
        f"  costo       ${r['costo_cop']:>7,.0f}  (presupuesto ${params.presupuesto_cop:,.0f})\n"
        f"  aptitud     {r['aptitud']:>8.4f}"
    )


if __name__ == "__main__":
    asyncio.run(main())
