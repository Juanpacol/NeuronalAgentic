"""Esquemas Pydantic para la API HTTP y los mensajes del WebSocket."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .ag.parametros import ParametrosAG


class TargetInfo(BaseModel):
    id: str
    nombre: str
    origen: str


class OpcionesParametros(BaseModel):
    seleccion: list[str]
    cruce: list[str]
    mutacion: list[str]
    operador_reordenamiento: list[str]
    defaults: dict[str, Any]


class MensajeIniciar(BaseModel):
    tipo: str = "iniciar"
    params: ParametrosAG | None = None
    target_id: str = "default"


class PuntoHistorial(BaseModel):
    generacion: int
    mejor: float
    promedio: float
