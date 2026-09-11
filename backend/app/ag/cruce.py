"""Operadores de cruce para permutaciones (TSP): variantes de Order Crossover (OX).

Los 3 nombres del curso (un_punto, dos_puntos, uniforme) se implementan aquí
como variantes de OX para garantizar que los hijos sean permutaciones válidas
(sin ciudades duplicadas ni faltantes) — un cruce ingenuo por posición
produciría rutas inválidas.
"""
from __future__ import annotations

import random

import numpy as np


def un_punto(p1: np.ndarray, p2: np.ndarray, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """OX de un punto de corte: [:c] viene de un padre, el resto se completa
    en el orden en que aparecen en el otro padre, saltando las ya usadas."""
    n = len(p1)
    c = rng.randrange(1, n)

    def hijo(base: np.ndarray, otro: np.ndarray) -> np.ndarray:
        usadas = set(base[:c].tolist())
        resto = [x for x in otro.tolist() if x not in usadas]
        return np.array(list(base[:c]) + resto, dtype=base.dtype)

    return hijo(p1, p2), hijo(p2, p1)


def dos_puntos(p1: np.ndarray, p2: np.ndarray, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """OX clásico de dos puntos: el segmento [c1:c2] se copia de un padre,
    el resto se rellena en orden cíclico desde el otro padre, escaneando a
    partir de c2 (convención estándar de OX) y saltando duplicados."""
    n = len(p1)
    c1, c2 = sorted(rng.sample(range(n), 2))
    orden_escaneo = list(range(c2, n)) + list(range(c2))
    posiciones_destino = list(range(c2, n)) + list(range(c1))

    def hijo(base: np.ndarray, otro: np.ndarray) -> np.ndarray:
        segmento = base[c1:c2]
        usadas = set(segmento.tolist())
        resto = [otro[i] for i in orden_escaneo if otro[i] not in usadas]
        resultado = np.empty(n, dtype=base.dtype)
        resultado[c1:c2] = segmento
        for pos, val in zip(posiciones_destino, resto):
            resultado[pos] = val
        return resultado

    return hijo(p1, p2), hijo(p2, p1)


def uniforme(p1: np.ndarray, p2: np.ndarray, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """Uniform Order Crossover (UOX): máscara aleatoria de posiciones a heredar
    de un padre, el resto se rellena en el orden del otro padre."""
    n = len(p1)
    mascara = [rng.random() < 0.5 for _ in range(n)]

    def hijo(base: np.ndarray, otro: np.ndarray) -> np.ndarray:
        resultado = np.full(n, -1, dtype=base.dtype)
        usadas = set()
        for i in range(n):
            if mascara[i]:
                resultado[i] = base[i]
                usadas.add(int(base[i]))
        resto = iter(x for x in otro.tolist() if x not in usadas)
        for i in range(n):
            if resultado[i] == -1:
                resultado[i] = next(resto)
        return resultado

    return hijo(p1, p2), hijo(p2, p1)
