"""Manejo de la población: creación y estadísticas de aptitud."""
from __future__ import annotations

import random

import numpy as np

from .representacion import crear_individuo


def crear_poblacion(n: int, num_triangulos: int, rng: random.Random) -> list[np.ndarray]:
    """Crea n individuos aleatorios."""
    return [crear_individuo(num_triangulos, rng) for _ in range(n)]


def estadisticas(aptitudes: np.ndarray) -> tuple[float, float, float]:
    """Devuelve (mejor, promedio, peor) de un array de aptitudes."""
    apt = np.asarray(aptitudes, dtype=np.float64)
    return float(apt.max()), float(apt.mean()), float(apt.min())
