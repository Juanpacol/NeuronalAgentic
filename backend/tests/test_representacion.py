import random

import numpy as np

from app.ag.representacion import GENES_POR_TRIANGULO, crear_individuo, decodificar


def test_longitud_y_rango():
    rng = random.Random(1)
    genoma = crear_individuo(80, rng)
    assert len(genoma) == 80 * GENES_POR_TRIANGULO
    assert genoma.dtype == np.float32
    assert np.all(genoma >= 0.0) and np.all(genoma <= 1.0)


def test_decodificacion():
    rng = random.Random(2)
    n = 5
    genoma = crear_individuo(n, rng)
    triangulos = decodificar(genoma)
    assert len(triangulos) == n
    for t in triangulos:
        assert len(t["puntos"]) == 3
        for p in t["puntos"]:
            assert len(p) == 2
            assert 0.0 <= p[0] <= 1.0
            assert 0.0 <= p[1] <= 1.0
        assert len(t["color"]) == 3
        for c in t["color"]:
            assert 0.0 <= c <= 1.0
        assert 0.0 <= t["alpha"] <= 1.0
