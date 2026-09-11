import pytest
from PIL import Image

from app.ag.fitness import preparar_objetivo
from app.ag.motor import evolucionar
from app.ag.parametros import ParametrosAG


def _objetivo():
    img = Image.new("RGB", (64, 64), (30, 120, 200))
    return preparar_objetivo(img, 32)


@pytest.mark.asyncio
async def test_mejor_aptitud_no_decreciente():
    params = ParametrosAG(
        poblacion=12,
        num_triangulos=10,
        elitismo=2,
        max_generaciones=30,
        resolucion_trabajo=32,
        criterio_parada="generaciones",
        seed=123,
    )
    objetivo = _objetivo()
    mejores = []
    async for estado in evolucionar(params, objetivo):
        mejores.append(estado.mejor_aptitud)
    assert len(mejores) == 31  # generaciones 0..30 inclusive
    for i in range(1, len(mejores)):
        assert mejores[i] >= mejores[i - 1] - 1e-9


@pytest.mark.asyncio
async def test_misma_seed_produce_series_identicas():
    params = ParametrosAG(
        poblacion=10,
        num_triangulos=8,
        elitismo=1,
        max_generaciones=15,
        resolucion_trabajo=32,
        seed=7,
    )
    objetivo = _objetivo()

    serie1 = [e.mejor_aptitud async for e in evolucionar(params, objetivo)]
    serie2 = [e.mejor_aptitud async for e in evolucionar(params, objetivo)]
    assert serie1 == serie2


@pytest.mark.asyncio
async def test_criterio_max_generaciones():
    params = ParametrosAG(
        poblacion=8, num_triangulos=6, max_generaciones=5,
        resolucion_trabajo=32, criterio_parada="generaciones", seed=1,
    )
    objetivo = _objetivo()
    razones = []
    async for estado in evolucionar(params, objetivo):
        if estado.razon_parada:
            razones.append(estado.razon_parada)
    assert razones == ["max_generaciones"]


@pytest.mark.asyncio
async def test_criterio_objetivo():
    params = ParametrosAG(
        poblacion=8, num_triangulos=6, max_generaciones=50,
        resolucion_trabajo=32, criterio_parada="objetivo",
        aptitud_objetivo=-1.0,  # se alcanza inmediatamente
        seed=1,
    )
    objetivo = _objetivo()
    ultima = None
    async for estado in evolucionar(params, objetivo):
        ultima = estado
    assert ultima.razon_parada == "aptitud_objetivo_alcanzada"
    assert ultima.generacion == 0


@pytest.mark.asyncio
async def test_criterio_convergencia():
    params = ParametrosAG(
        poblacion=8, num_triangulos=6, max_generaciones=200,
        resolucion_trabajo=32, criterio_parada="convergencia",
        paciencia=3, epsilon=1.0,  # epsilon enorme: nunca cuenta como mejora real
        seed=1,
    )
    objetivo = _objetivo()
    ultima = None
    async for estado in evolucionar(params, objetivo):
        ultima = estado
    assert ultima.razon_parada == "convergencia"
    assert ultima.generacion == 3


@pytest.mark.asyncio
async def test_detencion_externa():
    params = ParametrosAG(
        poblacion=8, num_triangulos=6, max_generaciones=200,
        resolucion_trabajo=32, seed=1,
    )
    objetivo = _objetivo()
    contador = {"n": 0}

    def debe_detener():
        contador["n"] += 1
        return contador["n"] > 3

    ultima = None
    async for estado in evolucionar(params, objetivo, debe_detener=debe_detener):
        ultima = estado
    assert ultima.razon_parada == "detenido_por_usuario"
