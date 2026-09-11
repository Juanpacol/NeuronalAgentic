import asyncio
from itertools import pairwise

import numpy as np
import pytest

from app.ag.alimentos import contexto_desde_parametros
from app.ag.motor import evolucionar
from app.ag.parametros import ParametrosAG


def _correr(params):
    ctx = contexto_desde_parametros(params)

    async def _run():
        return [e async for e in evolucionar(params, ctx)]

    return asyncio.run(_run())


def test_aptitud_mejor_no_decrece_con_elitismo():
    """Con elitismo >= 1 la mejor aptitud nunca puede empeorar entre generaciones."""
    params = ParametrosAG(seed=42, elitismo=3, max_generaciones=30,
                          criterio_parada="generaciones", poblacion=40)
    estados = _correr(params)
    aptitudes = [e.mejor_aptitud for e in estados]
    for anterior, actual in pairwise(aptitudes):
        assert actual >= anterior - 1e-12, "la mejor aptitud retrocedió"


def test_aptitud_mejora_de_verdad():
    """No basta con no empeorar: el AG debe efectivamente encontrar algo mejor."""
    params = ParametrosAG(seed=42, max_generaciones=60,
                          criterio_parada="generaciones", poblacion=40)
    estados = _correr(params)
    assert estados[-1].mejor_aptitud > estados[0].mejor_aptitud


def test_reproducibilidad_con_misma_semilla():
    params = ParametrosAG(seed=7, max_generaciones=20,
                          criterio_parada="generaciones", poblacion=30)
    a = [e.mejor_aptitud for e in _correr(params)]
    b = [e.mejor_aptitud for e in _correr(params)]
    assert a == b


def test_semillas_distintas_dan_series_distintas():
    p1 = ParametrosAG(seed=1, max_generaciones=20, criterio_parada="generaciones", poblacion=30)
    p2 = ParametrosAG(seed=2, max_generaciones=20, criterio_parada="generaciones", poblacion=30)
    assert [e.mejor_aptitud for e in _correr(p1)] != [e.mejor_aptitud for e in _correr(p2)]


def test_parada_por_max_generaciones():
    params = ParametrosAG(seed=1, max_generaciones=15,
                          criterio_parada="generaciones", poblacion=20)
    estados = _correr(params)
    assert estados[-1].razon_parada == "max_generaciones"
    assert estados[-1].generacion == 15


def test_parada_por_convergencia():
    params = ParametrosAG(seed=1, criterio_parada="convergencia", paciencia=5,
                          max_generaciones=500, poblacion=20)
    estados = _correr(params)
    assert estados[-1].razon_parada == "convergencia"
    assert estados[-1].generaciones_sin_mejora >= 5


def test_parada_por_aptitud_objetivo():
    """Mayor es mejor: se para al alcanzar el objetivo, no al bajar de él."""
    params = ParametrosAG(seed=1, criterio_parada="objetivo", aptitud_objetivo=0.60,
                          max_generaciones=500, poblacion=40)
    estados = _correr(params)
    assert estados[-1].razon_parada == "aptitud_objetivo_alcanzada"
    assert estados[-1].mejor_aptitud >= 0.60


def test_parada_externa():
    params = ParametrosAG(seed=1, max_generaciones=1000,
                          criterio_parada="generaciones", poblacion=20)
    ctx = contexto_desde_parametros(params)

    async def _run():
        estados = []
        async for e in evolucionar(params, ctx, debe_detener=lambda: len(estados) >= 5):
            estados.append(e)
        return estados

    estados = asyncio.run(_run())
    assert estados[-1].razon_parada == "detenido_por_usuario"


def test_estado_expone_lo_que_necesita_la_interfaz():
    params = ParametrosAG(seed=3, max_generaciones=5,
                          criterio_parada="generaciones", poblacion=20)
    e = _correr(params)[-1]
    assert set(e.macros_mejor) == {"kcal", "proteina_g", "carbohidratos_g", "grasa_g"}
    assert e.costo_mejor >= 0
    assert e.genoma_mejor is not None
    assert len(e.aptitudes) == params.poblacion
    # las aptitudes llegan ordenadas de mejor a peor, para la rejilla de población
    assert np.all(np.diff(e.aptitudes) <= 1e-12)


def test_genoma_mejor_respeta_las_cotas():
    params = ParametrosAG(seed=5, max_generaciones=40,
                          criterio_parada="generaciones", poblacion=30)
    ctx = contexto_desde_parametros(params)
    for e in _correr(params):
        assert np.all(e.genoma_mejor >= 0)
        assert np.all(e.genoma_mejor <= ctx.max_porciones)


@pytest.mark.parametrize("seleccion", ["proporcional", "torneo", "estocastica", "heuristica"])
def test_corre_con_cada_tecnica_de_seleccion(seleccion):
    params = ParametrosAG(seed=1, seleccion=seleccion, max_generaciones=10,
                          criterio_parada="generaciones", poblacion=20)
    assert len(_correr(params)) == 11


@pytest.mark.parametrize("cruce", ["un_punto", "dos_puntos", "uniforme"])
def test_corre_con_cada_tecnica_de_cruce(cruce):
    params = ParametrosAG(seed=1, cruce=cruce, max_generaciones=10,
                          criterio_parada="generaciones", poblacion=20)
    assert len(_correr(params)) == 11


@pytest.mark.parametrize("mutacion", ["heuristica", "intercambio", "desplazamiento", "insercion"])
def test_corre_con_cada_tecnica_de_mutacion(mutacion):
    params = ParametrosAG(seed=1, mutacion=mutacion, max_generaciones=10,
                          criterio_parada="generaciones", poblacion=20)
    assert len(_correr(params)) == 11
