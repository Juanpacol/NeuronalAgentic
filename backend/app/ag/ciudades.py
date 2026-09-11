"""Generación del mapa de ciudades y su matriz de distancias."""
from __future__ import annotations

import numpy as np


def generar_ciudades(num_ciudades: int, seed: int | None) -> np.ndarray:
    """Genera coordenadas (num_ciudades, 2) en [0,1], con su propio rng sembrado."""
    rng = np.random.default_rng(seed)
    return rng.random((num_ciudades, 2))


def calcular_matriz_distancias(ciudades: np.ndarray) -> np.ndarray:
    """Matriz (n,n) de distancias euclidianas, vectorizada por broadcasting."""
    diff = ciudades[:, None, :] - ciudades[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))
