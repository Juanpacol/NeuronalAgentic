"""Función objetivo: rasterizar el genoma y compararlo contra la imagen objetivo."""
from __future__ import annotations

from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageOps

from .representacion import GENES_POR_TRIANGULO, alpha_render


def rasterizar(genoma: np.ndarray, resolucion: int) -> Image.Image:
    """Dibuja todos los triángulos del genoma en un único ImageDraw.RGBA.

    Se evita alpha_composite por capas (es ~8x más lento); un solo
    ImageDraw.Draw(img, 'RGBA') con d.polygon(...) por triángulo basta porque
    Pillow ya mezcla el alpha del polígono contra el buffer RGBA subyacente.
    """
    img = Image.new("RGBA", (resolucion, resolucion), (0, 0, 0, 255))
    d = ImageDraw.Draw(img, "RGBA")
    n = len(genoma) // GENES_POR_TRIANGULO
    for i in range(n):
        bloque = genoma[i * GENES_POR_TRIANGULO:(i + 1) * GENES_POR_TRIANGULO]
        x1, y1, x2, y2, x3, y3, r, g, b, a = bloque
        puntos = [
            (float(x1) * resolucion, float(y1) * resolucion),
            (float(x2) * resolucion, float(y2) * resolucion),
            (float(x3) * resolucion, float(y3) * resolucion),
        ]
        color = (
            int(np.clip(r, 0, 1) * 255),
            int(np.clip(g, 0, 1) * 255),
            int(np.clip(b, 0, 1) * 255),
            int(np.clip(alpha_render(float(a)), 0, 1) * 255),
        )
        d.polygon(puntos, fill=color)
    return img


def preparar_objetivo(imagen: Image.Image, resolucion: int) -> np.ndarray:
    """Recorta a cuadrado y reescala la imagen objetivo a la resolución de trabajo."""
    imagen = imagen.convert("RGB")
    cuadrada = ImageOps.fit(imagen, (resolucion, resolucion), method=Image.LANCZOS)
    return np.array(cuadrada, dtype=np.uint8)


@lru_cache(maxsize=16)
def _preparar_objetivo_cacheado(ruta: str, resolucion: int) -> bytes:
    """Cachea el array preprocesado (como bytes, para poder usar lru_cache)."""
    imagen = Image.open(ruta)
    arr = preparar_objetivo(imagen, resolucion)
    return arr.tobytes()


def cargar_objetivo_desde_archivo(ruta: str, resolucion: int) -> np.ndarray:
    """Carga y cachea (por ruta+resolución) el objetivo preprocesado."""
    datos = _preparar_objetivo_cacheado(ruta, resolucion)
    return np.frombuffer(datos, dtype=np.uint8).reshape(resolucion, resolucion, 3)


def calcular_aptitud(genoma: np.ndarray, objetivo: np.ndarray, resolucion: int) -> float:
    """aptitud = 1 - RMSE_normalizado entre el render y el objetivo."""
    render = rasterizar(genoma, resolucion).convert("RGB")
    render_arr = np.array(render, dtype=np.int16)
    objetivo_arr = objetivo.astype(np.int16)
    error = render_arr - objetivo_arr
    rmse = np.sqrt(np.mean(error.astype(np.int64) ** 2))
    return 1.0 - rmse / 255.0
