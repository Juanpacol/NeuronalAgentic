import random

import numpy as np
import pytest

from app.ag.cruce import dos_puntos, un_punto, uniforme

TECNICAS = [un_punto, dos_puntos, uniforme]


@pytest.mark.parametrize("f_cruce", TECNICAS)
def test_longitud_correcta(f_cruce):
    rng = random.Random(0)
    p1 = np.random.RandomState(1).rand(100).astype(np.float32)
    p2 = np.random.RandomState(2).rand(100).astype(np.float32)
    h1, h2 = f_cruce(p1, p2, rng)
    assert len(h1) == 100
    assert len(h2) == 100


@pytest.mark.parametrize("f_cruce", TECNICAS)
def test_genes_provienen_de_padres(f_cruce):
    rng = random.Random(0)
    p1 = np.random.RandomState(1).rand(100).astype(np.float32)
    p2 = np.random.RandomState(2).rand(100).astype(np.float32)
    h1, h2 = f_cruce(p1, p2, rng)
    for h in (h1, h2):
        for i, gen in enumerate(h):
            assert gen == p1[i] or gen == p2[i]


@pytest.mark.parametrize("f_cruce", TECNICAS)
def test_padres_identicos_producen_hijos_identicos(f_cruce):
    rng = random.Random(0)
    p1 = np.random.RandomState(1).rand(100).astype(np.float32)
    p2 = p1.copy()
    h1, h2 = f_cruce(p1, p2, rng)
    assert np.array_equal(h1, p1)
    assert np.array_equal(h2, p1)


@pytest.mark.parametrize("f_cruce", TECNICAS)
def test_cruce_por_triangulo_respeta_frontera(f_cruce):
    rng = random.Random(0)
    p1 = np.random.RandomState(1).rand(100).astype(np.float32)
    p2 = np.random.RandomState(2).rand(100).astype(np.float32)
    h1, _ = f_cruce(p1, p2, rng, cruce_por_triangulo=True)
    # cada bloque de 10 genes debe provenir completamente de p1 o completamente de p2
    for i in range(10):
        bloque = h1[i * 10:(i + 1) * 10]
        de_p1 = np.array_equal(bloque, p1[i * 10:(i + 1) * 10])
        de_p2 = np.array_equal(bloque, p2[i * 10:(i + 1) * 10])
        assert de_p1 or de_p2
