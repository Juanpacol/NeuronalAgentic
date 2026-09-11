import random

import numpy as np

from app.ag.alimentos import contexto_desde_parametros
from app.ag.parametros import ParametrosAG
from app.ag.poblacion import crear_poblacion
from app.ag.representacion import crear_individuo, decodificar, recortar

CTX = contexto_desde_parametros(ParametrosAG())


def test_individuo_tiene_longitud_del_catalogo():
    g = crear_individuo(CTX.max_porciones, random.Random(0))
    assert len(g) == CTX.num_alimentos


def test_individuo_es_entero():
    g = crear_individuo(CTX.max_porciones, random.Random(0))
    assert np.issubdtype(g.dtype, np.integer)


def test_individuo_respeta_cotas_por_alimento():
    rng = random.Random(1)
    for _ in range(200):
        g = crear_individuo(CTX.max_porciones, rng)
        assert np.all(g >= 0)
        assert np.all(g <= CTX.max_porciones)


def test_individuo_es_reproducible_con_semilla():
    a = crear_individuo(CTX.max_porciones, random.Random(42))
    b = crear_individuo(CTX.max_porciones, random.Random(42))
    assert np.array_equal(a, b)


def test_recortar_lleva_a_las_cotas():
    fuera = CTX.max_porciones.astype(np.int32) + 10
    dentro = recortar(fuera, CTX.max_porciones)
    assert np.array_equal(dentro, CTX.max_porciones)

    negativo = np.full(CTX.num_alimentos, -5, dtype=np.int32)
    assert np.all(recortar(negativo, CTX.max_porciones) == 0)


def test_decodificar_devuelve_lista_de_enteros():
    g = crear_individuo(CTX.max_porciones, random.Random(3))
    d = decodificar(g)
    assert isinstance(d, list)
    assert all(isinstance(x, int) for x in d)
    assert d == [int(x) for x in g]


def test_poblacion_tiene_el_tamano_pedido():
    poblacion = crear_poblacion(25, CTX.max_porciones, random.Random(0))
    assert len(poblacion) == 25
    assert all(len(ind) == CTX.num_alimentos for ind in poblacion)
