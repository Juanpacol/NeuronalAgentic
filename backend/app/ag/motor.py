"""Motor del algoritmo genético: bucle evolutivo principal."""
from __future__ import annotations

import random
import time
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass

import numpy as np

from .fitness import calcular_aptitud
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
    genoma_mejor: np.ndarray | None
    tiempo_ms: float
    generaciones_sin_mejora: int
    razon_parada: str | None = None


def _kwargs_seleccion(params: ParametrosAG) -> dict:
    if params.seleccion == "torneo":
        return {"k": params.k_torneo}
    if params.seleccion == "heuristica":
        return {"num_mejores": params.num_mejores}
    return {}


def _kwargs_cruce(params: ParametrosAG) -> dict:
    return {"cruce_por_triangulo": params.cruce_por_triangulo}


def _aplicar_mutacion(genoma: np.ndarray, params: ParametrosAG, rng: random.Random) -> np.ndarray:
    f_mutacion = REGISTRO_MUTACION[params.mutacion]
    if params.mutacion == "heuristica":
        genoma = f_mutacion(genoma, params.prob_mutacion, rng, sigma=params.sigma_mutacion)
    else:
        genoma = f_mutacion(genoma, params.prob_mutacion, rng)

    # operador de reordenamiento opcional (adicional a la mutación principal)
    if params.operador_reordenamiento:
        f_reorden = REGISTRO_MUTACION[params.operador_reordenamiento]
        genoma = f_reorden(genoma, params.prob_reordenamiento, rng)
    return genoma


async def evolucionar(
    params: ParametrosAG,
    objetivo_arr: np.ndarray,
    debe_detener: Callable[[], bool] | None = None,
) -> AsyncIterator[EstadoGeneracion]:
    """Ejecuta el bucle evolutivo, cediendo un EstadoGeneracion por generación."""
    import asyncio

    rng = random.Random(params.seed)
    resolucion = params.resolucion_trabajo

    poblacion = crear_poblacion(params.poblacion, params.num_triangulos, rng)
    f_seleccion = REGISTRO_SELECCION[params.seleccion]
    f_cruce = REGISTRO_CRUCE[params.cruce]

    mejor_aptitud_historica = -np.inf
    generaciones_sin_mejora = 0
    generacion = 0

    while True:
        inicio = time.perf_counter()

        aptitudes = np.array(
            [calcular_aptitud(ind, objetivo_arr, resolucion) for ind in poblacion]
        )
        orden = np.argsort(-aptitudes)
        poblacion = [poblacion[i] for i in orden]
        aptitudes = aptitudes[orden]

        mejor, promedio, peor = estadisticas(aptitudes)

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
            genoma_mejor=poblacion[0].copy(),
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
        # se necesitan padres en pares
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
                h1, h2 = f_cruce(p1, p2, rng, **_kwargs_cruce(params))
            else:
                h1, h2 = p1.copy(), p2.copy()

            h1 = _aplicar_mutacion(h1, params, rng)
            nueva_poblacion.append(h1)
            if len(nueva_poblacion) < params.poblacion:
                h2 = _aplicar_mutacion(h2, params, rng)
                nueva_poblacion.append(h2)

            i += 2

        poblacion = nueva_poblacion
        generacion += 1

        await asyncio.sleep(0)
