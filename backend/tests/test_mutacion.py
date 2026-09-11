import random
from collections import Counter

import numpy as np
import pytest

from app.ag.alimentos import contexto_desde_parametros
from app.ag.mutacion import desplazamiento, heuristica, insercion, intercambio
from app.ag.parametros import ParametrosAG
from app.ag.representacion import crear_individuo

CTX = contexto_desde_parametros(ParametrosAG())
TECNICAS = [heuristica, intercambio, desplazamiento, insercion]


@pytest.mark.parametrize("f_mut", TECNICAS, ids=lambda f: f.__name__)
def test_respeta_cotas_y_tipo(f_mut):
    rng = random.Random(4)
    for _ in range(100):
        g = crear_individuo(CTX.max_porciones, rng)
        m = f_mut(g, 1.0, rng, ctx=CTX)
        assert len(m) == len(g)
        assert np.issubdtype(m.dtype, np.integer)
        assert np.all(m >= 0)
        assert np.all(m <= CTX.max_porciones)


@pytest.mark.parametrize("f_mut", TECNICAS, ids=lambda f: f.__name__)
def test_probabilidad_cero_es_identidad(f_mut):
    rng = random.Random(6)
    for _ in range(30):
        g = crear_individuo(CTX.max_porciones, rng)
        m = f_mut(g, 0.0, rng, ctx=CTX)
        assert np.array_equal(m, g)


@pytest.mark.parametrize("f_mut", TECNICAS, ids=lambda f: f.__name__)
def test_no_modifica_el_genoma_original(f_mut):
    rng = random.Random(8)
    g = crear_individuo(CTX.max_porciones, rng)
    copia = g.copy()
    f_mut(g, 1.0, rng, ctx=CTX)
    assert np.array_equal(g, copia)


@pytest.mark.parametrize("f_mut", TECNICAS, ids=lambda f: f.__name__)
def test_reproducible_con_misma_semilla(f_mut):
    g = crear_individuo(CTX.max_porciones, random.Random(10))
    a = f_mut(g, 0.5, random.Random(99), ctx=CTX)
    b = f_mut(g, 0.5, random.Random(99), ctx=CTX)
    assert np.array_equal(a, b)


def test_heuristica_hace_cambios_locales():
    """La perturbación gaussiana debe mover el genoma, no dejarlo igual."""
    rng = random.Random(12)
    g = crear_individuo(CTX.max_porciones, rng)
    cambios = 0
    for _ in range(50):
        m = heuristica(g, 1.0, rng, ctx=CTX)
        if not np.array_equal(m, g):
            cambios += 1
    assert cambios > 40


def test_intercambio_solo_mezcla_dentro_de_una_categoria():
    """El intercambio debe cambiar dos genes de la misma categoría, no de categorías distintas."""
    rng = random.Random(21)
    g = crear_individuo(CTX.max_porciones, rng)
    for _ in range(200):
        m = intercambio(g, 1.0, rng, ctx=CTX)
        distintos = np.where(m != g)[0]
        if len(distintos) == 0:
            continue  # ambos genes tenían el mismo valor
        categorias = {int(CTX.categorias[i]) for i in distintos}
        assert len(categorias) == 1, "el intercambio cruzó categorías"


def test_operadores_de_reordenamiento_preservan_el_multiconjunto():
    """desplazamiento e inserción solo reordenan: el conjunto de valores no cambia.

    Es justamente por esto que son casi arbitrarios en este dominio: mueven
    cantidades entre alimentos sin ninguna razón nutricional. El test documenta
    la propiedad, no la defiende como buena idea.
    """
    rng = random.Random(31)
    # Cotas uniformes: así el recorte no altera el multiconjunto y se puede
    # comprobar la propiedad de permutación en estado puro.
    max_porciones = np.full(CTX.num_alimentos, 4, dtype=np.int32)
    for f_mut in (desplazamiento, insercion):
        for _ in range(50):
            g = crear_individuo(max_porciones, rng)
            m = f_mut(g, 1.0, rng, ctx=None)
            assert Counter(g.tolist()) == Counter(m.tolist()), f_mut.__name__
