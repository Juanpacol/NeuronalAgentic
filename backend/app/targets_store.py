"""Almacén de imágenes objetivo: incluidas por defecto + subidas por el usuario (en memoria)."""
from __future__ import annotations

import io
import os
import uuid
from collections import OrderedDict

from PIL import Image

MAX_TAMANO_BYTES = 8 * 1024 * 1024
MAX_TARGETS_SUBIDOS = 16  # LRU simple

_DIR_TARGETS = os.path.join(os.path.dirname(__file__), "targets")

TARGETS_INCLUIDOS = {
    "default": {
        "nombre": "Retrato (curso)",
        "ruta": os.path.join(_DIR_TARGETS, "default.jpg"),
    },
}

# LRU simple: dict ordenado de target_id -> ruta o bytes en memoria
_subidos: OrderedDict[str, bytes] = OrderedDict()


def listar_targets() -> list:
    """Lista los targets disponibles: incluidos + subidos en esta sesión."""
    incluidos = [
        {"id": tid, "nombre": info["nombre"], "origen": "incluido"}
        for tid, info in TARGETS_INCLUIDOS.items()
    ]
    subidos = [
        {"id": tid, "nombre": f"Subido {tid[:8]}", "origen": "subido"}
        for tid in _subidos
    ]
    return incluidos + subidos


def guardar_target_subido(datos: bytes) -> str:
    """Valida, cachea (LRU) y devuelve el id de un target subido por el usuario."""
    if len(datos) > MAX_TAMANO_BYTES:
        raise ValueError("La imagen supera el tamaño máximo permitido (8MB)")
    # valida que sea una imagen decodificable
    Image.open(io.BytesIO(datos)).verify()

    target_id = uuid.uuid4().hex
    _subidos[target_id] = datos
    _subidos.move_to_end(target_id)
    while len(_subidos) > MAX_TARGETS_SUBIDOS:
        _subidos.popitem(last=False)
    return target_id


def obtener_imagen(target_id: str) -> Image.Image | None:
    """Devuelve la imagen PIL asociada a un target_id, o None si no existe."""
    if target_id in TARGETS_INCLUIDOS:
        return Image.open(TARGETS_INCLUIDOS[target_id]["ruta"])
    if target_id in _subidos:
        _subidos.move_to_end(target_id)
        return Image.open(io.BytesIO(_subidos[target_id]))
    return None
