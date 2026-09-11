"""Operadores de cruce sobre cromosomas planos (arrays numpy 1D)."""
from __future__ import annotations

import random

import numpy as np

from .representacion import GENES_POR_TRIANGULO


def _puntos_de_corte_validos(longitud: int, cruce_por_triangulo: bool) -> range:
    """Devuelve el rango de posiciones válidas para un punto de corte."""
    if cruce_por_triangulo:
        return range(GENES_POR_TRIANGULO, longitud, GENES_POR_TRIANGULO)
    return range(1, longitud)


def un_punto(p1: np.ndarray, p2: np.ndarray, rng: random.Random,
             cruce_por_triangulo: bool = False) -> tuple[np.ndarray, np.ndarray]:
    longitud = len(p1)
    candidatos = list(_puntos_de_corte_validos(longitud, cruce_por_triangulo))
    if not candidatos:
        return p1.copy(), p2.copy()
    c = rng.choice(candidatos)
    h1 = np.concatenate([p1[:c], p2[c:]]).astype(p1.dtype)
    h2 = np.concatenate([p2[:c], p1[c:]]).astype(p1.dtype)
    return h1, h2


def dos_puntos(p1: np.ndarray, p2: np.ndarray, rng: random.Random,
               cruce_por_triangulo: bool = False) -> tuple[np.ndarray, np.ndarray]:
    longitud = len(p1)
    candidatos = list(_puntos_de_corte_validos(longitud, cruce_por_triangulo))
    if len(candidatos) < 2:
        return un_punto(p1, p2, rng, cruce_por_triangulo)
    c1, c2 = sorted(rng.sample(candidatos, 2))
    h1 = np.concatenate([p1[:c1], p2[c1:c2], p1[c2:]]).astype(p1.dtype)
    h2 = np.concatenate([p2[:c1], p1[c1:c2], p2[c2:]]).astype(p1.dtype)
    return h1, h2


def uniforme(p1: np.ndarray, p2: np.ndarray, rng: random.Random,
             cruce_por_triangulo: bool = False) -> tuple[np.ndarray, np.ndarray]:
    longitud = len(p1)
    if cruce_por_triangulo:
        n_bloques = longitud // GENES_POR_TRIANGULO
        mascara_bloques = np.array([rng.random() < 0.5 for _ in range(n_bloques)])
        mascara = np.repeat(mascara_bloques, GENES_POR_TRIANGULO)
    else:
        mascara = np.array([rng.random() < 0.5 for _ in range(longitud)])
    h1 = np.where(mascara, p1, p2).astype(p1.dtype)
    h2 = np.where(mascara, p2, p1).astype(p1.dtype)
    return h1, h2
