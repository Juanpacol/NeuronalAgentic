"""Representación del cromosoma (C2): vector de porciones por alimento.

Cada individuo es un array de enteros de longitud `num_alimentos`, donde
`genoma[i]` son las porciones diarias del alimento `i` y `0` significa "no está
en la dieta".

Decisiones de diseño:

- Porciones ENTERAS, no gramos continuos: es la unidad que una persona lee
  ("2 huevos", "1 taza de arroz"), y los tres operadores de cruce son exactos
  sobre enteros.
- SIN gen de máscara aparte. Una máscara duplicaría el espacio de búsqueda y
  crearía codificaciones redundantes (máscara=0 con cantidad=7 describe el mismo
  fenotipo que máscara=1 con cantidad=0), un defecto clásico de diseño de AG.
- Cotas POR ALIMENTO (`max_porciones[i]`), no globales: 4 tazas de arroz es
  plausible, 4 aguacates no. Recortar a esas cotas tras cada operador es la
  única reparación que necesita todo el sistema.
"""
from __future__ import annotations

import random

import numpy as np


def crear_individuo(max_porciones: np.ndarray, rng: random.Random) -> np.ndarray:
    """Genoma aleatorio, entero uniforme en [0, max_porciones[i]] por gen.

    Esto produce dietas de 2–3x la meta calórica, y es deliberado: la curva de
    convergencia arranca visiblemente mal y sube, que es justo lo que necesita
    la tabla comparativa entre operadores. Sembrar individuos casi-factibles
    aplanaría las curvas y escondería las diferencias entre técnicas.
    """
    return np.array(
        [rng.randint(0, int(m)) for m in max_porciones], dtype=np.int32
    )


def recortar(genoma: np.ndarray, max_porciones: np.ndarray) -> np.ndarray:
    """Deja el genoma dentro de [0, max_porciones] y en dtype entero."""
    return np.clip(genoma, 0, max_porciones).astype(np.int32)


def decodificar(genoma: np.ndarray) -> list[int]:
    """Convierte el genoma en una lista serializable a JSON."""
    return [int(x) for x in genoma]
