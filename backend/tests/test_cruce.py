import random

import numpy as np
import pytest

from app.ag.alimentos import contexto_desde_parametros
from app.ag.cruce import dos_puntos, un_punto, uniforme
from app.ag.parametros import ParametrosAG
from app.ag.representacion import crear_individuo

CTX = contexto_desde_parametros(ParametrosAG())
TECNICAS = [un_punto, dos_puntos, uniforme]


def _padres(seed=0):
    rng = random.Random(seed)
    return crear_individuo(CTX.max_porciones, rng), crear_individuo(CTX.max_porciones, rng)


@pytest.mark.parametrize("f_cruce", TECNICAS, ids=lambda f: f.__name__)
def test_hijos_conservan_longitud_y_tipo(f_cruce):
    p1, p2 = _padres()
    h1, h2 = f_cruce(p1, p2, random.Random(5))
    for h in (h1, h2):
        assert len(h) == len(p1)
        assert np.issubdtype(h.dtype, np.integer)


@pytest.mark.parametrize("f_cruce", TECNICAS, ids=lambda f: f.__name__)
def test_cada_gen_proviene_de_algun_padre(f_cruce):
    """Propiedad que hace innecesaria la reparación: nada se inventa fuera de los padres."""
    p1, p2 = _padres(1)
    h1, h2 = f_cruce(p1, p2, random.Random(9))
    for h in (h1, h2):
        for i in range(len(h)):
            assert h[i] in (p1[i], p2[i])


@pytest.mark.parametrize("f_cruce", TECNICAS, ids=lambda f: f.__name__)
def test_hijos_respetan_las_cotas_sin_reparacion(f_cruce):
    """Si los padres respetan las cotas, los hijos también: el cruce es posicional."""
    rng = random.Random(11)
    for _ in range(50):
        p1 = crear_individuo(CTX.max_porciones, rng)
        p2 = crear_individuo(CTX.max_porciones, rng)
        h1, h2 = f_cruce(p1, p2, rng)
        for h in (h1, h2):
            assert np.all(h >= 0)
            assert np.all(h <= CTX.max_porciones)


@pytest.mark.parametrize("f_cruce", TECNICAS, ids=lambda f: f.__name__)
def test_padres_identicos_producen_hijos_identicos(f_cruce):
    p, _ = _padres(2)
    h1, h2 = f_cruce(p.copy(), p.copy(), random.Random(13))
    assert np.array_equal(h1, p)
    assert np.array_equal(h2, p)


@pytest.mark.parametrize("f_cruce", TECNICAS, ids=lambda f: f.__name__)
def test_reproducible_con_misma_semilla(f_cruce):
    p1, p2 = _padres(3)
    a1, a2 = f_cruce(p1, p2, random.Random(77))
    b1, b2 = f_cruce(p1, p2, random.Random(77))
    assert np.array_equal(a1, b1)
    assert np.array_equal(a2, b2)
