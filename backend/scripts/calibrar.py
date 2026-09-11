#!/usr/bin/env python3
"""Diagnóstico de calibración de la función objetivo.

Responde a una sola pregunta: ¿los dos términos de la penalización (macros y
costo) están ambos influyendo de verdad en la búsqueda, o uno es ruido?

Si un término es ruido, la comparación entre técnicas del informe pierde
sentido: el AG estaría optimizando una sola cosa mientras el enunciado afirma
que optimiza dos.

Uso: python scripts/calibrar.py   (ejecutado desde backend/)
"""
from __future__ import annotations

import asyncio
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ag.alimentos import contexto_desde_parametros  # noqa: E402
from app.ag.fitness import evaluar_poblacion  # noqa: E402
from app.ag.motor import evolucionar  # noqa: E402
from app.ag.parametros import ParametrosAG  # noqa: E402
from app.ag.representacion import crear_individuo  # noqa: E402

PESOS_A_PROBAR = [0.0, 0.1, 0.25, 0.5, 1.0]


async def _corrida(params):
    ctx = contexto_desde_parametros(params)
    serie = []
    async for e in evolucionar(params, ctx):
        serie.append(e)
    return ctx, serie


def diagnostico_correlacion(peso_costo: float) -> tuple[float, float]:
    """Sobre 1000 genomas aleatorios: ¿cuánto explica cada término la penalización total?"""
    import random

    params = ParametrosAG(peso_costo=peso_costo)
    ctx = contexto_desde_parametros(params)
    rng = random.Random(123)
    poblacion = [crear_individuo(ctx.max_porciones, rng) for _ in range(1000)]
    _, pen_macro, pen_costo, _ = evaluar_poblacion(poblacion, ctx)
    total = pen_macro + pen_costo

    def corr(x):
        # Un término constante (p. ej. pen_costo con peso 0) no correlaciona con
        # nada: su desviación estándar es 0. Se reporta como 0.0, que es la
        # lectura correcta —no influye— en vez de dejar que numpy devuelva nan.
        if np.std(x) == 0:
            return 0.0
        return float(np.corrcoef(x, total)[0, 1])

    return corr(pen_macro), corr(pen_costo)


async def main():
    print("=" * 78)
    print("1. CORRELACIÓN DE CADA TÉRMINO CON LA PENALIZACIÓN TOTAL")
    print("   (muestra aleatoria de 1000 genomas; ambos deberían superar 0.30)")
    print("=" * 78)
    print(f"{'peso_costo':>11} {'corr(macro)':>13} {'corr(costo)':>13}   veredicto")
    for w in PESOS_A_PROBAR:
        cm, cc = diagnostico_correlacion(w)
        if cc < 0.3:
            veredicto = "costo es RUIDO"
        elif cm < 0.3:
            veredicto = "el costo DOMINA"
        else:
            veredicto = "ambos influyen"
        print(f"{w:>11.2f} {cm:>13.3f} {cc:>13.3f}   {veredicto}")

    print()
    print("=" * 78)
    print("2. COMPORTAMIENTO A LO LARGO DE UNA CORRIDA REAL (400 generaciones)")
    print("=" * 78)
    print(f"{'peso_costo':>11} {'aptitud':>9} {'pen_macro':>11} {'pen_costo':>11} "
          f"{'costo':>9} {'kcal':>7} {'gen.conv':>9}")

    for w in PESOS_A_PROBAR:
        params = ParametrosAG(peso_costo=w, seed=42, max_generaciones=400,
                              criterio_parada="generaciones")
        _, serie = await _corrida(params)
        final = serie[-1]

        # primera generación que alcanza el 99% de la aptitud final
        umbral = final.mejor_aptitud * 0.99
        gen_conv = next(e.generacion for e in serie if e.mejor_aptitud >= umbral)

        print(
            f"{w:>11.2f} {final.mejor_aptitud:>9.4f} {final.pen_macro_mejor:>11.4f} "
            f"{final.pen_costo_mejor:>11.4f} {final.costo_mejor:>9,.0f} "
            f"{final.macros_mejor['kcal']:>7.0f} {gen_conv:>9}"
        )

    print()
    print("=" * 78)
    print("LECTURA DEL DIAGNÓSTICO")
    print("=" * 78)
    print(
        "- Si pen_costo se queda en 0.0000 durante toda la corrida, el costo no está\n"
        "  participando en la búsqueda: hay que subir peso_costo o bajar el presupuesto.\n"
        "- Si pen_macro se estanca mientras pen_costo sigue bajando, el costo domina y\n"
        "  el AG está sacrificando la nutrición para ahorrar: hay que bajar peso_costo.\n"
        "- El valor elegido debe dejar ambos términos vivos y las kcal cerca de la meta."
    )


if __name__ == "__main__":
    asyncio.run(main())
