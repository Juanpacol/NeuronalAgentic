"""Configuración de la aplicación vía variables de entorno."""
from __future__ import annotations

import os


def _origenes_permitidos() -> list:
    valor = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173")
    return [o.strip() for o in valor.split(",") if o.strip()]


PORT: int = int(os.environ.get("PORT", "8000"))
ALLOWED_ORIGINS: list = _origenes_permitidos()
MAX_RUNS_CONCURRENTES: int = int(os.environ.get("MAX_RUNS_CONCURRENTES", "2"))
