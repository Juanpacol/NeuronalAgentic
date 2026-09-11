"""Endpoint WebSocket /ws/evolucion: streaming de generaciones del algoritmo genético (TSP)."""
from __future__ import annotations

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .ag.ciudades import (
    calcular_matriz_distancias,
    generar_ciudades,
    generar_mapa_metro_medellin,
    nombres_metro_medellin,
)
from .ag.parametros import ParametrosAG
from .runner import RunManager

router = APIRouter()
run_manager = RunManager()


@router.websocket("/ws/evolucion")
async def ws_evolucion(websocket: WebSocket):
    await websocket.accept()

    task = None
    run = None
    try:
        while True:
            mensaje = await websocket.receive_json()
            tipo = mensaje.get("tipo")

            if tipo == "iniciar":
                if not run_manager.hay_capacidad():
                    await websocket.send_json({"tipo": "error", "codigo": "capacidad"})
                    await websocket.close()
                    return

                params_dict = mensaje.get("params") or {}
                params = ParametrosAG(**params_dict)

                nombres_ciudades = None
                if params.origen_ciudades == "metro_medellin":
                    ciudades = generar_mapa_metro_medellin()
                    nombres_ciudades = nombres_metro_medellin()
                else:
                    ciudades = generar_ciudades(params.num_ciudades, params.semilla_ciudades)
                matriz_distancias = calcular_matriz_distancias(ciudades)

                run = run_manager.crear_run(params)
                mensaje_iniciado = {
                    "tipo": "iniciado",
                    "run_id": run.run_id,
                    "ciudades": ciudades.tolist(),
                }
                if nombres_ciudades is not None:
                    mensaje_iniciado["nombres_ciudades"] = nombres_ciudades
                await websocket.send_json(mensaje_iniciado)

                async def enviar(msg, ws=websocket):
                    await ws.send_json(msg)

                task = asyncio.create_task(
                    run_manager.ejecutar(run, matriz_distancias, enviar)
                )
                run.task = task

            elif tipo == "pausar" and run is not None:
                run_manager.pausar(run.run_id)

            elif tipo == "reanudar" and run is not None:
                run_manager.reanudar(run.run_id)

            elif tipo == "detener" and run is not None:
                run_manager.detener(run.run_id)

    except WebSocketDisconnect:
        pass
    finally:
        if task is not None:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
