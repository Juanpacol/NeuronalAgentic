import asyncio

import numpy as np

from app.ag.ciudades import calcular_matriz_distancias, generar_ciudades
from app.ag.motor import evolucionar
from app.ag.parametros import ParametrosAG


def _correr(params: ParametrosAG, matriz: np.ndarray) -> list:
    async def _run():
        estados = []
        async for estado in evolucionar(params, matriz):
            estados.append(estado)
        return estados

    return asyncio.run(_run())


def _matriz_prueba(n=8, seed=1):
    ciudades = generar_ciudades(n, seed)
    return calcular_matriz_distancias(ciudades)


def test_distancia_mejor_no_crece():
    matriz = _matriz_prueba()
    params = ParametrosAG(
        poblacion=20, num_ciudades=8, elitismo=2, seed=42,
        criterio_parada="generaciones", max_generaciones=30,
    )
    estados = _correr(params, matriz)
    distancias = [e.distancia_mejor for e in estados]
    for i in range(1, len(distancias)):
        assert distancias[i] <= distancias[i - 1] + 1e-9


def test_reproducibilidad_con_misma_seed():
    matriz = _matriz_prueba()
    params = ParametrosAG(
        poblacion=20, num_ciudades=8, elitismo=2, seed=7,
        criterio_parada="generaciones", max_generaciones=15,
    )
    serie1 = [e.distancia_mejor for e in _correr(params, matriz)]
    serie2 = [e.distancia_mejor for e in _correr(params, matriz)]
    assert serie1 == serie2


def test_criterio_parada_generaciones():
    matriz = _matriz_prueba()
    params = ParametrosAG(
        poblacion=10, num_ciudades=6, seed=1,
        criterio_parada="generaciones", max_generaciones=5,
    )
    estados = _correr(params, matriz)
    assert estados[-1].razon_parada == "max_generaciones"
    assert estados[-1].generacion == 5


def test_criterio_parada_convergencia():
    matriz = _matriz_prueba()
    params = ParametrosAG(
        poblacion=10, num_ciudades=6, seed=1,
        criterio_parada="convergencia", paciencia=3, max_generaciones=500,
    )
    estados = _correr(params, matriz)
    assert estados[-1].razon_parada in ("convergencia", "max_generaciones")


def test_criterio_parada_objetivo():
    matriz = _matriz_prueba()
    params = ParametrosAG(
        poblacion=20, num_ciudades=6, seed=1,
        criterio_parada="objetivo", distancia_objetivo=100.0, max_generaciones=50,
    )
    estados = _correr(params, matriz)
    assert estados[-1].razon_parada == "distancia_objetivo_alcanzada"
