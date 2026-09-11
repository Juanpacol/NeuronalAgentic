"""Representación del cromosoma: permutación de ciudades.

Cada individuo es un array de enteros de longitud num_ciudades, una
permutación de [0, num_ciudades) que indica el orden en que se visitan.
"""
from __future__ import annotations

import random

import numpy as np


def crear_individuo(num_ciudades: int, rng: random.Random) -> np.ndarray:
    """Crea una permutación aleatoria de las ciudades."""
    orden = list(range(num_ciudades))
    rng.shuffle(orden)
    return np.array(orden, dtype=np.int32)


def decodificar(ruta: np.ndarray) -> list[int]:
    """Convierte la ruta (array de índices) en una lista serializable a JSON."""
    return [int(x) for x in ruta]
