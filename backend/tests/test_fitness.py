import random

import numpy as np
import pytest

from app.ag.alimentos import construir_contexto, contexto_desde_parametros
from app.ag.fitness import (
    calcular_aptitud,
    calcular_costo,
    calcular_macros,
    calcular_pen_costo,
    calcular_pen_macro,
    calcular_penalizacion,
    evaluar_poblacion,
)
from app.ag.parametros import ParametrosAG
from app.ag.representacion import crear_individuo

# Catálogo mínimo y con cifras redondas, para poder calcular a mano.
CATALOGO_PRUEBA = [
    {
        "codigo_tcac": "X001", "nombre": "Alimento A", "categoria": "carbohidratos",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 100.0, "proteina_g_100g": 10.0, "carbohidratos_g_100g": 10.0,
        "grasa_g_100g": 1.0, "precio_cop": 1000, "precio_verificado": False,
        "max_porciones": 5,
    },
    {
        "codigo_tcac": "X002", "nombre": "Alimento B", "categoria": "proteinas",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 200.0, "proteina_g_100g": 20.0, "carbohidratos_g_100g": 5.0,
        "grasa_g_100g": 2.0, "precio_cop": 2000, "precio_verificado": False,
        "max_porciones": 5,
    },
]


def _ctx_prueba(peso_costo=0.5, presupuesto=10000.0):
    return construir_contexto(
        objetivo_kcal=1000, objetivo_proteina_g=100,
        objetivo_carbohidratos_g=100, objetivo_grasa_g=10,
        peso_costo=peso_costo, presupuesto_cop=presupuesto,
        catalogo=CATALOGO_PRUEBA,
    )


def test_macros_y_costo_calculados_a_mano():
    ctx = _ctx_prueba()
    genoma = np.array([2, 3], dtype=np.int32)
    # 2 porciones de A (100 kcal c/u) + 3 de B (200 kcal c/u) = 800 kcal
    macros = calcular_macros(genoma, ctx)
    assert macros[0] == pytest.approx(800.0)
    assert macros[1] == pytest.approx(2 * 10 + 3 * 20)       # proteína = 80
    assert macros[2] == pytest.approx(2 * 10 + 3 * 5)        # carbos = 35
    assert macros[3] == pytest.approx(2 * 1 + 3 * 2)         # grasa = 8
    assert calcular_costo(genoma, ctx) == pytest.approx(2 * 1000 + 3 * 2000)


def test_penalizacion_exacta_calculada_a_mano():
    ctx = _ctx_prueba(peso_costo=0.5, presupuesto=10000.0)
    genoma = np.array([2, 3], dtype=np.int32)

    # desviaciones relativas contra las metas (1000, 100, 100, 10)
    dev = np.array([
        abs(800 - 1000) / 1000,   # 0.20
        abs(80 - 100) / 100,      # 0.20
        abs(35 - 100) / 100,      # 0.65
        abs(8 - 10) / 10,         # 0.20
    ])
    pesos = np.array([1.0, 1.0, 0.8, 0.8]) / 3.6
    esperado_macro = float(pesos @ dev)
    assert calcular_pen_macro(genoma, ctx) == pytest.approx(esperado_macro)

    # costo 8000 sobre presupuesto 10000: el término proporcional cobra 0.8 del
    # presupuesto y la bisagra no cobra nada porque no hay exceso.
    esperado_costo = 0.5 * (8000 / 10000 + 2.0 * 0.0)
    assert calcular_pen_costo(genoma, ctx) == pytest.approx(esperado_costo)

    total = esperado_macro + esperado_costo
    assert calcular_penalizacion(genoma, ctx) == pytest.approx(total)
    assert calcular_aptitud(genoma, ctx) == pytest.approx(1 / (1 + total))


def test_mas_barato_siempre_es_mejor():
    """El costo debe ser un gradiente continuo, no solo un castigo al pasarse.

    Sin esta propiedad el AG no optimiza "al menor costo" sino apenas "sin
    pasarse del presupuesto", que no es el objetivo del problema. Es justo el
    fallo que detectó la calibración en la primera versión de la fórmula.
    """
    ctx = _ctx_prueba(peso_costo=0.5, presupuesto=10000.0)
    anterior = None
    for porciones in range(0, 5):
        g = np.array([porciones, 0], dtype=np.int32)
        actual = calcular_pen_costo(g, ctx)
        if anterior is not None:
            assert actual > anterior, "gastar más debe penalizar más, siempre"
        anterior = actual


def test_exceder_presupuesto_penaliza_extra_sin_anular_la_aptitud():
    """La bisagra hace que pasarse sea claramente peor, pero sin acantilado."""
    ctx = _ctx_prueba(peso_costo=0.5, presupuesto=5000.0)

    barato = np.array([1, 1], dtype=np.int32)     # 3000 COP, bajo presupuesto
    esperado_barato = 0.5 * (3000 / 5000)
    assert calcular_pen_costo(barato, ctx) == pytest.approx(esperado_barato)

    caro = np.array([5, 5], dtype=np.int32)       # 15000 COP, 10000 de exceso
    esperado_caro = 0.5 * (15000 / 5000 + 2.0 * 10000 / 5000)
    assert calcular_pen_costo(caro, ctx) == pytest.approx(esperado_caro)

    # el exceso cobra más que la simple proporción, pero no anula la aptitud:
    # sigue habiendo gradiente por el que el AG puede bajar
    assert esperado_caro > 0.5 * (15000 / 5000)
    assert calcular_aptitud(caro, ctx) > 0.0


def test_aptitud_en_rango_valido():
    ctx = _ctx_prueba()
    rng = random.Random(0)
    for _ in range(100):
        g = crear_individuo(ctx.max_porciones, rng)
        a = calcular_aptitud(g, ctx)
        assert 0.0 < a <= 1.0


def test_aptitud_maxima_con_dieta_perfecta():
    """Con los macros exactos y sin presión de costo, la aptitud llega a 1."""
    ctx = construir_contexto(
        objetivo_kcal=100, objetivo_proteina_g=10,
        objetivo_carbohidratos_g=10, objetivo_grasa_g=1,
        peso_costo=0.0, presupuesto_cop=10000, catalogo=CATALOGO_PRUEBA,
    )
    genoma = np.array([1, 0], dtype=np.int32)
    assert calcular_aptitud(genoma, ctx) == pytest.approx(1.0)


def test_monotonia_ante_empeoramiento_conocido():
    """Alejarse de la meta debe bajar la aptitud, sin excepción."""
    ctx = construir_contexto(
        objetivo_kcal=100, objetivo_proteina_g=10,
        objetivo_carbohidratos_g=10, objetivo_grasa_g=1,
        peso_costo=0.0, presupuesto_cop=10_000_000, catalogo=CATALOGO_PRUEBA,
    )
    anterior = calcular_aptitud(np.array([1, 0], dtype=np.int32), ctx)
    for porciones in range(2, 6):
        actual = calcular_aptitud(np.array([porciones, 0], dtype=np.int32), ctx)
        assert actual < anterior
        anterior = actual


def test_evaluar_poblacion_coincide_con_evaluacion_individual():
    """La versión vectorizada debe dar exactamente lo mismo que la individual."""
    ctx = _ctx_prueba()
    rng = random.Random(7)
    poblacion = [crear_individuo(ctx.max_porciones, rng) for _ in range(30)]

    aptitudes, pen_macro, pen_costo, costos = evaluar_poblacion(poblacion, ctx)

    for i, g in enumerate(poblacion):
        assert aptitudes[i] == pytest.approx(calcular_aptitud(g, ctx))
        assert pen_macro[i] == pytest.approx(calcular_pen_macro(g, ctx))
        assert pen_costo[i] == pytest.approx(calcular_pen_costo(g, ctx))
        assert costos[i] == pytest.approx(calcular_costo(g, ctx))


def test_calibracion_ambos_terminos_influyen():
    """Con el catálogo y los parámetros reales, ni los macros ni el costo pueden ser ruido.

    Si alguien edita el catálogo o desbalancea peso_costo hasta el punto de que
    un término deja de correlacionar con la penalización total, la comparación
    entre técnicas del informe pierde sentido. Este test lo detecta.
    """
    ctx = contexto_desde_parametros(ParametrosAG())
    rng = random.Random(123)
    poblacion = [crear_individuo(ctx.max_porciones, rng) for _ in range(1000)]

    _, pen_macro, pen_costo, _ = evaluar_poblacion(poblacion, ctx)
    total = pen_macro + pen_costo

    corr_macro = float(np.corrcoef(pen_macro, total)[0, 1])
    corr_costo = float(np.corrcoef(pen_costo, total)[0, 1])

    assert corr_macro > 0.3, f"la penalización por macros es ruido (corr={corr_macro:.2f})"
    assert corr_costo > 0.3, f"la penalización por costo es ruido (corr={corr_costo:.2f})"
