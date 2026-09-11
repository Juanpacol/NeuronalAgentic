"""Esquemas Pydantic para la API HTTP y los mensajes del WebSocket."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .ag.parametros import ParametrosAG


class OpcionesParametros(BaseModel):
    seleccion: list[str]
    cruce: list[str]
    mutacion: list[str]
    defaults: dict[str, Any]


class MensajeIniciar(BaseModel):
    tipo: str = "iniciar"
    params: ParametrosAG | None = None


class PuntoHistorial(BaseModel):
    generacion: int
    mejor: float
    promedio: float
