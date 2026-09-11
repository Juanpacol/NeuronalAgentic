"""Motor del algoritmo genético: bucle evolutivo principal (optimización de dieta)."""
from __future__ import annotations

import random
import time
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass

import numpy as np

from .alimentos import ContextoDieta
from .fitness import evaluar_poblacion
from .parada import evaluar_parada
from .parametros import ParametrosAG
from .poblacion import crear_poblacion, estadisticas
from .registry import REGISTRO_CRUCE, REGISTRO_MUTACION, REGISTRO_SELECCION


@dataclass
class EstadoGeneracion:
    generacion: int
    mejor_aptitud: float
    aptitud_promedio: float
    aptitud_peor: float
    costo_mejor: float
    desviacion_mejor: float
    pen_macro_mejor: float
    pen_costo_mejor: float
    macros_mejor: dict
    genoma_mejor: np.ndarray | None
    aptitudes: np.ndarray | None
    tiempo_ms: float
    generaciones_sin_mejora: int
    razon_parada: str | None = None


def _kwargs_seleccion(params: ParametrosAG) -> dict:
    if params.seleccion == "torneo":
        return {"k": params.k_torneo}
    if params.seleccion == "heuristica":
        return {"num_mejores": params.num_mejores}
    return {}


def _aplicar_mutacion(
    genoma: np.ndarray, params: ParametrosAG, rng: random.Random, ctx: ContextoDieta
) -> np.ndarray:
    f_mutacion = REGISTRO_MUTACION[params.mutacion]
    return f_mutacion(genoma, params.prob_mutacion, rng, ctx=ctx)


async def evolucionar(
    params: ParametrosAG,
    ctx: ContextoDieta,
    debe_detener: Callable[[], bool] | None = None,
) -> AsyncIterator[EstadoGeneracion]:
    """Ejecuta el bucle evolutivo, cediendo un EstadoGeneracion por generación."""
    import asyncio

    rng = random.Random(params.seed)

    poblacion = crear_poblacion(params.poblacion, ctx.max_porciones, rng)
    f_seleccion = REGISTRO_SELECCION[params.seleccion]
    f_cruce = REGISTRO_CRUCE[params.cruce]

    mejor_aptitud_historica = -np.inf
    generaciones_sin_mejora = 0
    generacion = 0

    while True:
        inicio = time.perf_counter()

        # Evaluación vectorizada de la población entera (un solo (N,n)@(n,4)).
        aptitudes, pen_macro, pen_costo, costos = evaluar_poblacion(poblacion, ctx)

        orden = np.argsort(-aptitudes)
        poblacion = [poblacion[i] for i in orden]
        aptitudes = aptitudes[orden]
        pen_macro = pen_macro[orden]
        pen_costo = pen_costo[orden]
        costos = costos[orden]

        mejor, promedio, peor = estadisticas(aptitudes)

        genoma_mejor = poblacion[0]
        macros = ctx.matriz_nutrientes.T @ genoma_mejor.astype(np.float64)

        if mejor > mejor_aptitud_historica + params.epsilon:
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora += 1
        mejor_aptitud_historica = max(mejor_aptitud_historica, mejor)

        tiempo_ms = (time.perf_counter() - inicio) * 1000.0

        detener_externo = debe_detener() if debe_detener else False
        razon = evaluar_parada(
            params, generacion, mejor, generaciones_sin_mejora, detener_externo
        )

        estado = EstadoGeneracion(
            generacion=generacion,
            mejor_aptitud=mejor,
            aptitud_promedio=promedio,
            aptitud_peor=peor,
            costo_mejor=float(costos[0]),
            desviacion_mejor=float(pen_macro[0]),
            pen_macro_mejor=float(pen_macro[0]),
            pen_costo_mejor=float(pen_costo[0]),
            macros_mejor={
                "kcal": float(macros[0]),
                "proteina_g": float(macros[1]),
                "carbohidratos_g": float(macros[2]),
                "grasa_g": float(macros[3]),
            },
            genoma_mejor=genoma_mejor.copy(),
            aptitudes=aptitudes.copy(),
            tiempo_ms=tiempo_ms,
            generaciones_sin_mejora=generaciones_sin_mejora,
            razon_parada=razon,
        )
        yield estado

        if razon is not None:
            return

        # --- construir nueva generación ---
        nueva_poblacion: list[np.ndarray] = [ind.copy() for ind in poblacion[: params.elitismo]]

        n_padres = params.poblacion - params.elitismo
        n_padres_par = n_padres + (n_padres % 2)
        indices_padres = f_seleccion(
            poblacion, aptitudes, n_padres_par, rng, **_kwargs_seleccion(params)
        )

        i = 0
        while len(nueva_poblacion) < params.poblacion:
            i1 = indices_padres[i % len(indices_padres)]
            i2 = indices_padres[(i + 1) % len(indices_padres)]
            p1, p2 = poblacion[i1], poblacion[i2]

            if rng.random() < params.prob_cruce:
                h1, h2 = f_cruce(p1, p2, rng)
            else:
                h1, h2 = p1.copy(), p2.copy()

            h1 = _aplicar_mutacion(h1, params, rng, ctx)
            nueva_poblacion.append(h1)
            if len(nueva_poblacion) < params.poblacion:
                h2 = _aplicar_mutacion(h2, params, rng, ctx)
                nueva_poblacion.append(h2)

            i += 2

        poblacion = nueva_poblacion
        generacion += 1

        if params.retardo_ms > 0:
            await asyncio.sleep(params.retardo_ms / 1000.0)
        else:
            await asyncio.sleep(0)
