import random

import numpy as np
from PIL import Image

from app.ag.fitness import calcular_aptitud, preparar_objetivo, rasterizar
from app.ag.representacion import crear_individuo


def test_render_identico_al_objetivo_da_aptitud_alta():
    rng = random.Random(3)
    genoma = crear_individuo(60, rng)
    render = rasterizar(genoma, 64).convert("RGB")
    objetivo = np.array(render, dtype=np.uint8)
    aptitud = calcular_aptitud(genoma, objetivo, 64)
    assert aptitud > 0.999


def test_imagen_distinta_da_aptitud_baja():
    rng = random.Random(4)
    genoma = crear_individuo(60, rng)
    objetivo = np.zeros((64, 64, 3), dtype=np.uint8)
    objetivo[:, :] = [255, 255, 255]
    # genoma completamente negro (r,g,b=0) sobre fondo blanco -> muy distinto
    genoma_negro = genoma.copy()
    for i in range(60):
        genoma_negro[i * 10 + 6] = 0.0
        genoma_negro[i * 10 + 7] = 0.0
        genoma_negro[i * 10 + 8] = 0.0
        genoma_negro[i * 10 + 9] = 1.0
    aptitud = calcular_aptitud(genoma_negro, objetivo, 64)
    assert aptitud < 0.5


def test_monotonia_respecto_a_ruido():
    rng = random.Random(5)
    genoma = crear_individuo(60, rng)
    render = rasterizar(genoma, 64).convert("RGB")
    objetivo = np.array(render, dtype=np.uint8)

    aptitud_base = calcular_aptitud(genoma, objetivo, 64)

    rng_ruido = np.random.RandomState(0)
    aptitud_previa = aptitud_base
    for nivel in (0.05, 0.15, 0.3):
        # promediar varias corridas por nivel para evitar ruido de una sola muestra
        aptitudes_nivel = []
        for _ in range(5):
            ruidoso = genoma + rng_ruido.normal(0, nivel, size=genoma.shape).astype(np.float32)
            ruidoso = np.clip(ruidoso, 0.0, 1.0).astype(np.float32)
            aptitudes_nivel.append(calcular_aptitud(ruidoso, objetivo, 64))
        aptitud_ruidosa = float(np.mean(aptitudes_nivel))
        assert aptitud_ruidosa <= aptitud_previa + 1e-6
        aptitud_previa = aptitud_ruidosa


def test_preparar_objetivo_devuelve_resolucion_correcta():
    img = Image.new("RGB", (200, 100), (10, 20, 30))
    arr = preparar_objetivo(img, 64)
    assert arr.shape == (64, 64, 3)
