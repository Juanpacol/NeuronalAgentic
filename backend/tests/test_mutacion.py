import random

import numpy as np
import pytest

from app.ag import mutacion


def _permutacion_valida(salida: np.ndarray, n: int) -> bool:
    return len(salida) == n and set(salida.tolist()) == set(range(n))


OPERADORES = [mutacion.intercambio, mutacion.desplazamiento, mutacion.insercion]


@pytest.mark.parametrize("operador", OPERADORES)
def test_mutacion_preserva_permutacion_valida(operador):
    rng = random.Random(3)
    n = 10
    genoma = np.random.default_rng(5).permutation(n).astype(np.int32)
    for _ in range(20):
        salida = operador(genoma, 1.0, rng)
        assert _permutacion_valida(salida, n)


@pytest.mark.parametrize("operador", OPERADORES)
def test_prob_cero_es_identidad(operador):
    rng = random.Random(4)
    genoma = np.arange(9, dtype=np.int32)
    salida = operador(genoma, 0.0, rng)
    assert np.array_equal(salida, genoma)


def test_heuristica_sin_matriz_es_permutacion_valida():
    rng = random.Random(6)
    n = 8
    genoma = np.random.default_rng(9).permutation(n).astype(np.int32)
    salida = mutacion.heuristica(genoma, 1.0, rng)
    assert _permutacion_valida(salida, n)


def test_heuristica_con_matriz_mejora_o_iguala_distancia():
    from app.ag.ciudades import calcular_matriz_distancias, generar_ciudades
    from app.ag.fitness import calcular_distancia_ruta

    rng = random.Random(11)
    ciudades = generar_ciudades(8, seed=1)
    matriz = calcular_matriz_distancias(ciudades)
    genoma = np.random.default_rng(2).permutation(8).astype(np.int32)
    dist_antes = calcular_distancia_ruta(genoma, matriz)
    salida = mutacion.heuristica(genoma, 1.0, rng, matriz_distancias=matriz)
    dist_despues = calcular_distancia_ruta(salida, matriz)
    assert dist_despues <= dist_antes
    assert _permutacion_valida(salida, 8)


def test_heuristica_prob_cero_es_identidad():
    rng = random.Random(4)
    genoma = np.arange(9, dtype=np.int32)
    salida = mutacion.heuristica(genoma, 0.0, rng)
    assert np.array_equal(salida, genoma)
