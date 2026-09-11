"""Representación del cromosoma: array plano float32 de N*10 genes.

Cada bloque de 10 genes describe un triángulo semitransparente:
[x1, y1, x2, y2, x3, y3, r, g, b, a] con todos los valores en [0, 1].
"""
from __future__ import annotations

import random

import numpy as np

GENES_POR_TRIANGULO = 10
ALPHA_MIN = 0.10
ALPHA_ESCALA = 0.55


def crear_individuo(num_triangulos: int, rng: random.Random) -> np.ndarray:
    """Crea un genoma aleatorio de longitud num_triangulos * 10."""
    n = num_triangulos * GENES_POR_TRIANGULO
    return np.array([rng.random() for _ in range(n)], dtype=np.float32)


def alpha_render(a: float) -> float:
    """Mapea el gen de alpha [0,1] al alpha real usado al renderizar."""
    return ALPHA_MIN + ALPHA_ESCALA * a


def decodificar(genoma: np.ndarray) -> list:
    """Convierte el genoma plano en una lista de triángulos serializables a JSON."""
    triangulos = []
    n = len(genoma) // GENES_POR_TRIANGULO
    for i in range(n):
        bloque = genoma[i * GENES_POR_TRIANGULO:(i + 1) * GENES_POR_TRIANGULO]
        x1, y1, x2, y2, x3, y3, r, g, b, a = (float(v) for v in bloque)
        triangulos.append({
            "puntos": [[x1, y1], [x2, y2], [x3, y3]],
            "color": [r, g, b],
            "alpha": a,
        })
    return triangulos
