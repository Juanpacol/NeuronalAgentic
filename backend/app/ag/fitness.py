"""Función objetivo: distancia total de la ruta (menor = mejor) y aptitud derivada."""
from __future__ import annotations

import numpy as np


def calcular_distancia_ruta(ruta: np.ndarray, matriz_distancias: np.ndarray) -> float:
    """Suma de distancias consecutivas + regreso al origen (ciclo cerrado)."""
    siguiente = np.roll(ruta, -1)
    return float(matriz_distancias[ruta, siguiente].sum())


def calcular_aptitud(ruta: np.ndarray, matriz_distancias: np.ndarray) -> float:
    """Mayor = mejor, para reusar selección/elitismo sin cambios: 1/(1+distancia)."""
    return 1.0 / (1.0 + calcular_distancia_ruta(ruta, matriz_distancias))
