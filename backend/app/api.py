"""Endpoints HTTP: salud, opciones de parámetros, targets, historial de corridas."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, UploadFile

from . import targets_store
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


@router.get("/api/targets")
async def listar_targets():
    return targets_store.listar_targets()


@router.post("/api/target")
async def subir_target(archivo: UploadFile):
    datos = await archivo.read()
    if len(datos) > targets_store.MAX_TAMANO_BYTES:
        raise HTTPException(status_code=413, detail="La imagen supera 8MB")
    try:
        target_id = targets_store.guardar_target_subido(datos)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"target_id": target_id}


@router.get("/api/runs/{run_id}/historial")
async def historial(run_id: str):
    run = run_manager.obtener(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Corrida no encontrada")
    return run_manager.obtener_historial(run_id)
