"""Endpoints HTTP: salud, opciones de parámetros, historial de corridas."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .ag.parametros import ParametrosAG
from .ag.registry import nombres_disponibles
from .ws import run_manager

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/api/parametros/opciones")
async def opciones_parametros():
    opciones = nombres_disponibles()
    opciones["defaults"] = ParametrosAG().model_dump()
    return opciones


@router.get("/api/runs/{run_id}/historial")
async def historial(run_id: str):
    run = run_manager.obtener(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Corrida no encontrada")
    return run_manager.obtener_historial(run_id)
