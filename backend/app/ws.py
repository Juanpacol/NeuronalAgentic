"""Endpoint WebSocket /ws/evolucion: streaming de generaciones del AG de dieta."""
from __future__ import annotations

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .ag.alimentos import catalogo_serializable, contexto_desde_parametros
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
                ctx = contexto_desde_parametros(params)

                run = run_manager.crear_run(params)
                await websocket.send_json({
                    "tipo": "iniciado",
                    "run_id": run.run_id,
                    "alimentos": catalogo_serializable(),
                    "objetivos": {
                        "kcal": params.objetivo_kcal,
                        "proteina_g": params.objetivo_proteina_g,
                        "carbohidratos_g": params.objetivo_carbohidratos_g,
                        "grasa_g": params.objetivo_grasa_g,
                        "presupuesto_cop": params.presupuesto_cop,
                    },
                })

                async def enviar(msg, ws=websocket):
                    await ws.send_json(msg)

                task = asyncio.create_task(run_manager.ejecutar(run, ctx, enviar))
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
