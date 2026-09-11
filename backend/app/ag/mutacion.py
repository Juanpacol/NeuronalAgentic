"""Operadores de mutación para permutaciones (TSP).

Todos reciben (genoma, prob, rng) y devuelven una nueva ruta (permutación
válida). A diferencia de la versión de aproximación de imágenes, aquí los
cuatro operadores son literales y correctos para el problema: TSP es
exactamente el dominio para el que se diseñaron intercambio/desplazamiento/
inserción/heurística en la literatura clásica de AG.
"""
from __future__ import annotations

import random

import numpy as np


def intercambio(genoma: np.ndarray, prob: float, rng: random.Random) -> np.ndarray:
    """Mutación de intercambio (swap): intercambia dos ciudades de posición."""
    salida = genoma.copy()
    if rng.random() < prob:
        i, j = rng.sample(range(len(salida)), 2)
        salida[i], salida[j] = salida[j], salida[i]
    return salida


def desplazamiento(genoma: np.ndarray, prob: float, rng: random.Random) -> np.ndarray:
    """Mutación de desplazamiento: toma un segmento contiguo y lo mueve a otra posición."""
    salida = genoma.copy()
    n = len(salida)
    if rng.random() < prob and n > 3:
        i = rng.randrange(n)
        largo = rng.randint(1, max(1, n // 4))
        indices_segmento = {(i + k) % n for k in range(largo)}
        segmento = [salida[(i + k) % n] for k in range(largo)]
        resto = [x for idx, x in enumerate(salida) if idx not in indices_segmento]
        destino = rng.randrange(len(resto) + 1)
        nueva = resto[:destino] + segmento + resto[destino:]
        salida = np.array(nueva, dtype=genoma.dtype)
    return salida


def insercion(genoma: np.ndarray, prob: float, rng: random.Random) -> np.ndarray:
    """Mutación de inserción: extrae una ciudad y la reinserta en otra posición."""
    salida = list(genoma)
    if rng.random() < prob and len(salida) > 2:
        origen, destino = rng.sample(range(len(salida)), 2)
        ciudad = salida.pop(origen)
        salida.insert(destino, ciudad)
    return np.array(salida, dtype=genoma.dtype)


def heuristica(
    genoma: np.ndarray,
    prob: float,
    rng: random.Random,
    matriz_distancias: np.ndarray | None = None,
) -> np.ndarray:
    """Mutación heurística: prueba varios intercambios candidatos y se queda con
    el que más reduce la distancia de la ruta (2-opt simplificado por muestreo).
    Sin matriz_distancias degrada a un intercambio simple aleatorio."""
    salida = genoma.copy()
    if rng.random() >= prob:
        return salida

    n = len(salida)
    if matriz_distancias is None or n < 4:
        i, j = rng.sample(range(n), 2)
        salida[i], salida[j] = salida[j], salida[i]
        return salida

    from .fitness import calcular_distancia_ruta

    mejor_dist = calcular_distancia_ruta(salida, matriz_distancias)
    mejor_candidato = salida
    for _ in range(5):
        candidato = salida.copy()
        i, j = rng.sample(range(n), 2)
        candidato[i], candidato[j] = candidato[j], candidato[i]
        dist = calcular_distancia_ruta(candidato, matriz_distancias)
        if dist < mejor_dist:
            mejor_dist = dist
            mejor_candidato = candidato
    return mejor_candidato
