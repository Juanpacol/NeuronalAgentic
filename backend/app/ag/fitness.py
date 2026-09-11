"""Función objetivo (C3): qué tan bien una dieta cumple las metas, al menor costo.

Convención clave: MAYOR APTITUD ES MEJOR, mediante `aptitud = 1/(1+penalización)`.
Gracias a ella `seleccion.py` funciona sin un solo cambio respecto al dominio
anterior: sus cuatro operadores solo suponen que una aptitud mayor es preferible.
"""
from __future__ import annotations

import numpy as np

from .alimentos import ContextoDieta


def calcular_macros(genoma: np.ndarray, ctx: ContextoDieta) -> np.ndarray:
    """Totales de [kcal, proteína, carbohidratos, grasa] de la dieta."""
    return ctx.matriz_nutrientes.T @ genoma.astype(np.float64)


def calcular_costo(genoma: np.ndarray, ctx: ContextoDieta) -> float:
    """Costo total de la dieta en COP."""
    return float(ctx.precios @ genoma.astype(np.float64))


def calcular_desviacion_macros(genoma: np.ndarray, ctx: ContextoDieta) -> np.ndarray:
    """Error relativo por macronutriente: |logrado - meta| / meta. Adimensional."""
    totales = calcular_macros(genoma, ctx)
    return np.abs(totales - ctx.objetivos) / ctx.objetivos


def calcular_pen_macro(genoma: np.ndarray, ctx: ContextoDieta) -> float:
    """Penalización por alejarse de las metas nutricionales."""
    return float(ctx.pesos_macro @ calcular_desviacion_macros(genoma, ctx))


def calcular_pen_costo(genoma: np.ndarray, ctx: ContextoDieta) -> float:
    """Penalización por costo: término proporcional + bisagra por exceso.

    El diseño original solo tenía la bisagra `max(0, costo - presupuesto)`. La
    calibración (scripts/calibrar.py) demostró que así el costo era RUIDO: la
    mejor dieta costaba ~$7.300 contra un presupuesto de $20.000, la bisagra
    nunca se activaba y `pen_costo` valía 0.0000 en todas las generaciones. Peor
    aún, sin término proporcional el AG no tiene ningún incentivo para bajar del
    presupuesto, así que no optimizaba "al menor costo" sino solo "sin pasarse",
    que no es el objetivo declarado del problema.

    Se añade entonces `costo / presupuesto`, que hace que más barato siempre sea
    mejor y convierte al costo en el desempate real entre dietas nutricionalmente
    equivalentes. La bisagra se conserva, con peso doble, para que exceder el
    presupuesto siga siendo claramente peor que acercarse a él.

    Sigue siendo penalización blanda y no restricción dura: un corte seco
    (aptitud 0 sobre el presupuesto) crearía un acantilado que destruye la
    información de gradiente y degenera la selección proporcional.
    """
    costo = calcular_costo(genoma, ctx)
    exceso = max(0.0, costo - ctx.presupuesto)
    proporcional = costo / ctx.presupuesto
    return float(ctx.peso_costo * (proporcional + 2.0 * exceso / ctx.presupuesto))


def calcular_penalizacion(genoma: np.ndarray, ctx: ContextoDieta) -> float:
    return calcular_pen_macro(genoma, ctx) + calcular_pen_costo(genoma, ctx)


def calcular_aptitud(genoma: np.ndarray, ctx: ContextoDieta) -> float:
    """Aptitud en (0, 1]: 1.0 es la dieta perfecta (metas exactas y dentro de presupuesto)."""
    return 1.0 / (1.0 + calcular_penalizacion(genoma, ctx))


def evaluar_poblacion(
    poblacion: list[np.ndarray], ctx: ContextoDieta
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Evalúa la población entera de una vez.

    Apila en (N, n_alimentos) y hace un solo producto (N,n)@(n,4), en vez de
    recorrer individuo por individuo. Deja el paso de evaluación prácticamente
    gratis frente al resto del bucle evolutivo.

    Devuelve (aptitudes, penalizaciones_macro, penalizaciones_costo, costos).
    """
    matriz = np.asarray(poblacion, dtype=np.float64)          # (N, n)
    totales = matriz @ ctx.matriz_nutrientes                   # (N, 4)

    desviaciones = np.abs(totales - ctx.objetivos) / ctx.objetivos
    pen_macro = desviaciones @ ctx.pesos_macro                 # (N,)

    costos = matriz @ ctx.precios                              # (N,)
    excesos = np.maximum(0.0, costos - ctx.presupuesto)
    pen_costo = ctx.peso_costo * (
        costos / ctx.presupuesto + 2.0 * excesos / ctx.presupuesto
    )                                                          # (N,)

    aptitudes = 1.0 / (1.0 + pen_macro + pen_costo)
    return aptitudes, pen_macro, pen_costo, costos


def resumen_dieta(genoma: np.ndarray, ctx: ContextoDieta) -> dict:
    """Desglose legible del individuo, para la interfaz y los scripts."""
    macros = calcular_macros(genoma, ctx)
    return {
        "macros": {
            "kcal": float(macros[0]),
            "proteina_g": float(macros[1]),
            "carbohidratos_g": float(macros[2]),
            "grasa_g": float(macros[3]),
        },
        "costo_cop": calcular_costo(genoma, ctx),
        "pen_macro": calcular_pen_macro(genoma, ctx),
        "pen_costo": calcular_pen_costo(genoma, ctx),
        "aptitud": calcular_aptitud(genoma, ctx),
        "porciones": [
            {"nombre": ctx.nombres[i], "porciones": int(genoma[i])}
            for i in range(len(genoma))
            if genoma[i] > 0
        ],
    }
