import random

import numpy as np
import pytest

from app.ag import cruce

TECNICAS = [cruce.un_punto, cruce.dos_puntos, cruce.uniforme]


def _permutacion_valida(hijo: np.ndarray, n: int) -> bool:
    return len(hijo) == n and set(hijo.tolist()) == set(range(n))


@pytest.mark.parametrize("tecnica", TECNICAS)
def test_hijos_son_permutaciones_validas(tecnica):
    rng = random.Random(42)
    n = 10
    p1 = np.random.default_rng(1).permutation(n).astype(np.int32)
    p2 = np.random.default_rng(2).permutation(n).astype(np.int32)
    for _ in range(20):
        h1, h2 = tecnica(p1, p2, rng)
        assert _permutacion_valida(h1, n)
        assert _permutacion_valida(h2, n)


@pytest.mark.parametrize("tecnica", TECNICAS)
def test_padres_identicos_producen_hijos_identicos(tecnica):
    rng = random.Random(7)
    n = 8
    p = np.arange(n, dtype=np.int32)
    h1, h2 = tecnica(p, p.copy(), rng)
    assert np.array_equal(h1, p)
    assert np.array_equal(h2, p)
