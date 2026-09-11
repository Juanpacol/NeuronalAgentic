"""Operadores de selección de padres. Todos reciben (poblacion, aptitudes, n_padres, rng)
y devuelven una lista de índices (con repetición) hacia `poblacion`.
"""
from __future__ import annotations

import random
from collections.abc import Sequence

import numpy as np


def proporcional(poblacion: Sequence, aptitudes: Sequence[float], n_padres: int,
                  rng: random.Random) -> list[int]:
    """Selección por ruleta. Se desplazan las aptitudes para evitar valores negativos."""
    apt = np.asarray(aptitudes, dtype=np.float64)
    minimo = apt.min()
    if minimo < 0:
        apt = apt - minimo
    total = apt.sum()
    if total <= 0:
        # todas las aptitudes iguales (o cero): selección uniforme
        return [rng.randrange(len(poblacion)) for _ in range(n_padres)]
    probs = apt / total
    acumulada = np.cumsum(probs)
    elegidos = []
    for _ in range(n_padres):
        r = rng.random()
        idx = int(np.searchsorted(acumulada, r, side="right"))
        idx = min(idx, len(poblacion) - 1)
        elegidos.append(idx)
    return elegidos


def torneo(poblacion: Sequence, aptitudes: Sequence[float], n_padres: int,
           rng: random.Random, k: int = 3) -> list[int]:
    """Torneo: se eligen k individuos al azar y gana el de mayor aptitud."""
    elegidos = []
    n = len(poblacion)
    for _ in range(n_padres):
        candidatos = [rng.randrange(n) for _ in range(k)]
        mejor = max(candidatos, key=lambda i: aptitudes[i])
        elegidos.append(mejor)
    return elegidos


def estocastica(poblacion: Sequence, aptitudes: Sequence[float], n_padres: int,
                 rng: random.Random) -> list[int]:
    """Selección universal estocástica (SUS): un solo offset aleatorio,
    punteros equiespaciados sobre la suma acumulada de aptitudes."""
    apt = np.asarray(aptitudes, dtype=np.float64)
    minimo = apt.min()
    if minimo < 0:
        apt = apt - minimo
    total = apt.sum()
    n = len(poblacion)
    if total <= 0:
        return [rng.randrange(n) for _ in range(n_padres)]
    paso = total / n_padres
    inicio = rng.random() * paso
    acumulada = np.cumsum(apt)
    elegidos = []
    idx = 0
    for i in range(n_padres):
        puntero = inicio + i * paso
        while idx < n - 1 and acumulada[idx] < puntero:
            idx += 1
        elegidos.append(idx)
    return elegidos


def heuristica(poblacion: Sequence, aptitudes: Sequence[float], n_padres: int,
               rng: random.Random, num_mejores: int = 10) -> list[int]:
    """Truncamiento elitista: los padres solo se eligen entre el top num_mejores."""
    orden = sorted(range(len(poblacion)), key=lambda i: aptitudes[i], reverse=True)
    lista_seleccionados = orden[:num_mejores]
    if not lista_seleccionados:
        lista_seleccionados = orden
    return [rng.choice(lista_seleccionados) for _ in range(n_padres)]
