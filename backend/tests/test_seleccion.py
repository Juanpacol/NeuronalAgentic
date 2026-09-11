import random
from collections import Counter

import numpy as np
import pytest

from app.ag.seleccion import estocastica, heuristica, proporcional, torneo


def _poblacion_ficticia(n):
    return [np.zeros(1) for _ in range(n)]


@pytest.mark.parametrize("f_sel", [proporcional, torneo, estocastica, heuristica])
def test_indices_validos(f_sel):
    rng = random.Random(0)
    poblacion = _poblacion_ficticia(10)
    aptitudes = [rng.random() for _ in range(10)]
    indices = f_sel(poblacion, aptitudes, 20, rng)
    assert len(indices) == 20
    assert all(0 <= i < 10 for i in indices)


@pytest.mark.parametrize("f_sel", [proporcional, estocastica])
def test_favorece_al_mejor(f_sel):
    rng = random.Random(42)
    n = 10
    poblacion = _poblacion_ficticia(n)
    aptitudes = [0.0] * (n - 1) + [1.0]
    conteo = Counter()
    for _ in range(200):
        indices = f_sel(poblacion, aptitudes, 5, rng)
        conteo.update(indices)
    assert conteo[n - 1] == max(conteo.values())
    assert conteo[n - 1] > 0.5 * sum(conteo.values())
