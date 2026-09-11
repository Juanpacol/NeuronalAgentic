import random

from app.ag.representacion import crear_individuo, decodificar


def test_crear_individuo_es_permutacion_valida():
    rng = random.Random(1)
    n = 12
    ind = crear_individuo(n, rng)
    assert len(ind) == n
    assert set(ind.tolist()) == set(range(n))


def test_decodificar_es_identidad():
    rng = random.Random(2)
    ind = crear_individuo(8, rng)
    decodificado = decodificar(ind)
    assert decodificado == [int(x) for x in ind]
    assert all(isinstance(x, int) for x in decodificado)
