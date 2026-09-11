"""Operadores de mutación (C4c) sobre el vector de porciones.

NOTA HONESTA PARA EL INFORME
----------------------------
De los cuatro operadores que pide el curso, solo dos tienen sentido pleno sobre
un cromosoma de cantidades:

- `heuristica`  -> con sentido pleno. Es la mutación natural de un vector de
                   cantidades: búsqueda local en la vecindad del individuo.
- `intercambio` -> con sentido DENTRO DE CATEGORÍA. Intercambiar las porciones
                   de arroz y pollo es absurdo nutricionalmente; intercambiar
                   arroz y arepa (ambos carbohidratos) es un movimiento real de
                   "sustituir un básico por otro".
- `desplazamiento` y `insercion` -> CASI ARBITRARIOS. Son operadores de
                   permutación: presuponen que la posición de un gen significa
                   algo. Aquí la posición es solo el índice del alimento en el
                   catálogo, un orden convencional sin contenido. Se implementan
                   por completitud frente al requisito de la asignatura y se
                   espera que rindan peor que los dos anteriores. La tabla
                   comparativa del informe debería mostrarlo: eso es un
                   resultado del experimento, no un fallo de la implementación.
"""
from __future__ import annotations

import random

import numpy as np

from .alimentos import ContextoDieta
from .representacion import recortar


def heuristica(
    genoma: np.ndarray, prob: float, rng: random.Random, ctx: ContextoDieta | None = None
) -> np.ndarray:
    """Perturbación gaussiana por gen: g += round(N(0, sigma)), recortado a las cotas.

    sigma es proporcional a la cota del alimento (0.15 * max_porciones[i]), para
    que un alimento con cota 4 se explore con pasos mayores que uno con cota 2.
    """
    salida = genoma.astype(np.int32).copy()
    if ctx is None:
        # Sin contexto no se conocen las cotas; se degrada a un paso unitario.
        for i in range(len(salida)):
            if rng.random() < prob:
                salida[i] = max(0, salida[i] + rng.choice([-1, 1]))
        return salida

    max_porciones = ctx.max_porciones
    for i in range(len(salida)):
        if rng.random() < prob:
            sigma = max(0.5, 0.15 * float(max_porciones[i]))
            salida[i] = salida[i] + round(rng.gauss(0, sigma))
    return recortar(salida, max_porciones)


def intercambio(
    genoma: np.ndarray, prob: float, rng: random.Random, ctx: ContextoDieta | None = None
) -> np.ndarray:
    """Intercambia las porciones de dos alimentos de la MISMA categoría.

    Con sentido nutricional: equivale a sustituir un básico por otro comparable
    (arroz por arepa), no a cambiar proteína por carbohidrato.
    """
    salida = genoma.astype(np.int32).copy()
    if rng.random() >= prob:
        return salida

    if ctx is None:
        i, j = rng.sample(range(len(salida)), 2)
        salida[i], salida[j] = salida[j], salida[i]
        return salida

    # Solo categorías con al menos dos alimentos admiten intercambio.
    candidatas = [idx for idx in ctx.indices_por_categoria.values() if len(idx) >= 2]
    if not candidatas:
        return salida
    grupo = candidatas[rng.randrange(len(candidatas))]
    i, j = rng.sample(list(grupo), 2)
    salida[i], salida[j] = salida[j], salida[i]
    # El intercambio puede violar cotas: dos alimentos de la misma categoría
    # pueden tener max_porciones distintos (p. ej. arroz 4 vs avena 3).
    return recortar(salida, ctx.max_porciones) if ctx is not None else salida


def desplazamiento(
    genoma: np.ndarray, prob: float, rng: random.Random, ctx: ContextoDieta | None = None
) -> np.ndarray:
    """Rotación circular de un segmento contiguo de genes.

    Operador de permutación: el orden del catálogo NO es una dimensión con
    significado, así que este movimiento es casi arbitrario. Incluido por
    completitud frente al requisito del curso; se espera que rinda peor.
    """
    salida = genoma.astype(np.int32).copy()
    n = len(salida)
    if rng.random() >= prob or n < 3:
        return salida

    i = rng.randrange(n)
    largo = rng.randint(2, max(2, n // 3))
    indices = [(i + k) % n for k in range(largo)]
    valores = [int(salida[k]) for k in indices]
    corrimiento = rng.randint(1, largo - 1)
    rotados = valores[corrimiento:] + valores[:corrimiento]
    for k, v in zip(indices, rotados):
        salida[k] = v

    return recortar(salida, ctx.max_porciones) if ctx is not None else salida


def insercion(
    genoma: np.ndarray, prob: float, rng: random.Random, ctx: ContextoDieta | None = None
) -> np.ndarray:
    """Extrae el valor de un gen y lo reinserta en otra posición, desplazando el resto.

    Operador de permutación: igual que `desplazamiento`, el orden del catálogo no
    significa nada, así que el movimiento es casi arbitrario. Incluido por
    completitud frente al requisito del curso; se espera que rinda peor.
    """
    salida = genoma.astype(np.int32).copy()
    n = len(salida)
    if rng.random() >= prob or n < 2:
        return salida

    valores = [int(x) for x in salida]
    origen, destino = rng.sample(range(n), 2)
    v = valores.pop(origen)
    valores.insert(destino, v)
    salida = np.array(valores, dtype=np.int32)

    return recortar(salida, ctx.max_porciones) if ctx is not None else salida
