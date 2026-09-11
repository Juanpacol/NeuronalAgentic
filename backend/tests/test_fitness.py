import numpy as np
import pytest

from app.ag.fitness import calcular_aptitud, calcular_distancia_ruta

# Cuadrado unitario: 4 ciudades en las esquinas.
CIUDADES = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
])


def _matriz_distancias(ciudades: np.ndarray) -> np.ndarray:
    diff = ciudades[:, None, :] - ciudades[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


def test_distancia_ruta_perimetro_del_cuadrado():
    matriz = _matriz_distancias(CIUDADES)
    ruta = np.array([0, 1, 2, 3], dtype=np.int32)  # recorre el perímetro
    distancia = calcular_distancia_ruta(ruta, matriz)
    assert distancia == pytest.approx(4.0)


def test_distancia_ruta_en_diagonal_es_mayor():
    matriz = _matriz_distancias(CIUDADES)
    perimetro = calcular_distancia_ruta(np.array([0, 1, 2, 3], dtype=np.int32), matriz)
    cruzada = calcular_distancia_ruta(np.array([0, 2, 1, 3], dtype=np.int32), matriz)
    assert cruzada > perimetro


def test_aptitud_mayor_cuando_distancia_menor():
    matriz = _matriz_distancias(CIUDADES)
    buena = np.array([0, 1, 2, 3], dtype=np.int32)
    mala = np.array([0, 2, 1, 3], dtype=np.int32)
    assert calcular_aptitud(buena, matriz) > calcular_aptitud(mala, matriz)
