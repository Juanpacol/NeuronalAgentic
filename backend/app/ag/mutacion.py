"""Operadores de mutación. Todos reciben (genoma, prob, rng) y devuelven un nuevo genoma."""
from __future__ import annotations

import random

import numpy as np

from .representacion import GENES_POR_TRIANGULO


def heuristica(genoma: np.ndarray, prob: float, rng: random.Random,
               sigma: float = 0.1) -> np.ndarray:
    """Mutación gaussiana: gen += N(0, sigma), recortado a [0,1].

    Es el operador por defecto: el único que explora color/posición de verdad.
    """
    salida = genoma.copy()
    for i in range(len(salida)):
        if rng.random() < prob:
            salida[i] = np.clip(salida[i] + rng.gauss(0, sigma), 0.0, 1.0)
    return salida.astype(genoma.dtype)


def intercambio(genoma: np.ndarray, prob: float, rng: random.Random) -> np.ndarray:
    """Intercambia dos triángulos completos (bloques de 10 genes).

    Operador de reordenamiento de capas (algoritmo del pintor): neutro en
    píxeles cuando los triángulos no se solapan, solo cambia el orden de dibujo.
    """
    salida = genoma.copy()
    n_bloques = len(salida) // GENES_POR_TRIANGULO
    if n_bloques < 2:
        return salida
    if rng.random() < prob:
        i, j = rng.sample(range(n_bloques), 2)
        bi = slice(i * GENES_POR_TRIANGULO, (i + 1) * GENES_POR_TRIANGULO)
        bj = slice(j * GENES_POR_TRIANGULO, (j + 1) * GENES_POR_TRIANGULO)
        salida[bi], salida[bj] = salida[bj].copy(), salida[bi].copy()
    return salida


def desplazamiento(genoma: np.ndarray, prob: float, rng: random.Random) -> np.ndarray:
    """Rota un bloque de triángulos k posiciones.

    Operador de reordenamiento de capas (algoritmo del pintor): neutro en
    píxeles cuando los triángulos no se solapan, solo cambia el orden de dibujo.
    """
    salida = genoma.copy()
    n_bloques = len(salida) // GENES_POR_TRIANGULO
    if n_bloques < 2:
        return salida
    if rng.random() < prob:
        bloques = salida.reshape(n_bloques, GENES_POR_TRIANGULO)
        k = rng.randrange(1, n_bloques)
        bloques = np.roll(bloques, k, axis=0)
        salida = bloques.reshape(-1)
    return salida


def insercion(genoma: np.ndarray, prob: float, rng: random.Random) -> np.ndarray:
    """Extrae un triángulo y lo reinserta en otro índice.

    Operador de reordenamiento de capas (algoritmo del pintor): neutro en
    píxeles cuando los triángulos no se solapan, solo cambia el orden de dibujo.
    """
    salida = genoma.copy()
    n_bloques = len(salida) // GENES_POR_TRIANGULO
    if n_bloques < 2:
        return salida
    if rng.random() < prob:
        bloques = list(salida.reshape(n_bloques, GENES_POR_TRIANGULO))
        origen, destino = rng.sample(range(n_bloques), 2)
        bloque = bloques.pop(origen)
        bloques.insert(destino, bloque)
        salida = np.stack(bloques).reshape(-1)
    return salida
