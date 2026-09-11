import numpy as np

from app.ag.ciudades import (
    ESTACIONES_METRO_MEDELLIN,
    calcular_matriz_distancias,
    generar_ciudades,
    generar_mapa_metro_medellin,
    nombres_metro_medellin,
)


def test_generar_mapa_metro_medellin_forma_y_rango():
    ciudades = generar_mapa_metro_medellin()
    assert ciudades.shape == (len(ESTACIONES_METRO_MEDELLIN), 2)
    assert ciudades.min() >= -1e-9
    assert ciudades.max() <= 1 + 1e-9


def test_generar_mapa_metro_medellin_preserva_proporcion():
    """El mapa real es más largo en un eje que en el otro (Medellín es alargada
    norte-sur); no debe distorsionarse a un cuadrado perfecto."""
    ciudades = generar_mapa_metro_medellin()
    ancho = ciudades[:, 0].max() - ciudades[:, 0].min()
    alto = ciudades[:, 1].max() - ciudades[:, 1].min()
    assert ancho != alto


def test_nombres_metro_medellin_coincide_en_longitud():
    nombres = nombres_metro_medellin()
    ciudades = generar_mapa_metro_medellin()
    assert len(nombres) == len(ciudades)
    assert "San Antonio" in nombres


def test_matriz_distancias_metro_medellin_es_simetrica_y_sin_diagonal():
    ciudades = generar_mapa_metro_medellin()
    matriz = calcular_matriz_distancias(ciudades)
    assert matriz.shape == (len(ciudades), len(ciudades))
    assert np.allclose(matriz, matriz.T)
    assert np.allclose(np.diag(matriz), 0.0)


def test_generar_ciudades_aleatorio_sigue_funcionando():
    ciudades = generar_ciudades(10, seed=1)
    assert ciudades.shape == (10, 2)
