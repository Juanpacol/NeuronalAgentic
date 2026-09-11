"""Operadores de cruce (C4b) sobre el vector de porciones.

Sobre un cromosoma posicional de enteros, los tres operadores del curso son los
de manual y NO necesitan ninguna reparación: si ambos padres respetan las cotas
`[0, max_porciones[i]]`, cualquier combinación posicional de sus genes también
las respeta, porque cada gen conserva su posición —y por tanto su cota.

Es una simplificación estricta frente al dominio anterior (TSP), donde hacía
falta un Order Crossover completo solo para no producir rutas con ciudades
repetidas o faltantes.
"""
from __future__ import annotations

import random

import numpy as np


def un_punto(p1: np.ndarray, p2: np.ndarray, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """Un punto de corte: el hijo toma la cabeza de un padre y la cola del otro."""
    n = len(p1)
    if n < 2:
        return p1.copy(), p2.copy()
    c = rng.randrange(1, n)
    h1 = np.concatenate([p1[:c], p2[c:]]).astype(np.int32)
    h2 = np.concatenate([p2[:c], p1[c:]]).astype(np.int32)
    return h1, h2


def dos_puntos(p1: np.ndarray, p2: np.ndarray, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """Dos puntos de corte: se intercambia el segmento central."""
    n = len(p1)
    if n < 3:
        return un_punto(p1, p2, rng)
    c1, c2 = sorted(rng.sample(range(1, n), 2))
    h1 = np.concatenate([p1[:c1], p2[c1:c2], p1[c2:]]).astype(np.int32)
    h2 = np.concatenate([p2[:c1], p1[c1:c2], p2[c2:]]).astype(np.int32)
    return h1, h2


def uniforme(p1: np.ndarray, p2: np.ndarray, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """Máscara aleatoria: cada gen se hereda de uno u otro padre con igual probabilidad."""
    n = len(p1)
    mascara = np.array([rng.random() < 0.5 for _ in range(n)])
    h1 = np.where(mascara, p1, p2).astype(np.int32)
    h2 = np.where(mascara, p2, p1).astype(np.int32)
    return h1, h2
