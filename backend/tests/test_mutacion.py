import random
from collections import Counter

import numpy as np
import pytest

from app.ag.mutacion import desplazamiento, heuristica, insercion, intercambio

REORDENAMIENTO = [intercambio, desplazamiento, insercion]


@pytest.mark.parametrize("f_mut", [heuristica, intercambio, desplazamiento, insercion])
def test_salida_en_rango(f_mut):
    rng = random.Random(0)
    genoma = np.random.RandomState(1).rand(100).astype(np.float32)
    salida = f_mut(genoma, 0.5, rng)
    assert np.all(salida >= 0.0) and np.all(salida <= 1.0)
    assert len(salida) == 100


@pytest.mark.parametrize("f_mut", [heuristica, intercambio, desplazamiento, insercion])
def test_prob_cero_es_identidad(f_mut):
    rng = random.Random(0)
    genoma = np.random.RandomState(1).rand(100).astype(np.float32)
    salida = f_mut(genoma, 0.0, rng)
    assert np.array_equal(salida, genoma)


@pytest.mark.parametrize("f_mut", REORDENAMIENTO)
def test_reordenamiento_preserva_multiconjunto_de_bloques(f_mut):
    rng = random.Random(0)
    genoma = np.random.RandomState(1).rand(100).astype(np.float32)

    def bloques_como_tuplas(g):
        return Counter(
            tuple(round(float(v), 6) for v in g[i * 10:(i + 1) * 10])
            for i in range(10)
        )

    salida = f_mut(genoma, 1.0, rng)
    assert bloques_como_tuplas(salida) == bloques_como_tuplas(genoma)
