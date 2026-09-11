"""Gestión de corridas del algoritmo genético: una asyncio.Task por conexión WS."""
from __future__ import annotations

import asyncio
import uuid

import numpy as np

from . import config
from .ag.motor import EstadoGeneracion, evolucionar
from .ag.parametros import ParametrosAG
from .ag.representacion import decodificar


class Run:
    def __init__(self, run_id: str, params: ParametrosAG):
        self.run_id = run_id
        self.params = params
        self.pausa = asyncio.Event()
        self.pausa.set()  # corriendo por defecto
        self.detener_flag = False
        self.historial: list[dict] = []
        self.ultimo_mejor: float | None = None
        self.task: asyncio.Task | None = None
        self.terminado = False
        self.razon: str | None = None


class RunManager:
    """Administra las corridas activas del algoritmo genético."""

    def __init__(self, max_runs: int | None = None):
        self.max_runs = max_runs if max_runs is not None else config.MAX_RUNS_CONCURRENTES
        self._runs: dict[str, Run] = {}

    def cantidad_activas(self) -> int:
        return sum(1 for r in self._runs.values() if not r.terminado)

    def hay_capacidad(self) -> bool:
        return self.cantidad_activas() < self.max_runs

    def crear_run(self, params: ParametrosAG) -> Run:
        run_id = uuid.uuid4().hex
        run = Run(run_id, params)
        self._runs[run_id] = run
        return run

    def obtener(self, run_id: str) -> Run | None:
        return self._runs.get(run_id)

    def pausar(self, run_id: str) -> None:
        run = self._runs.get(run_id)
        if run:
            run.pausa.clear()

    def reanudar(self, run_id: str) -> None:
        run = self._runs.get(run_id)
        if run:
            run.pausa.set()

    def detener(self, run_id: str) -> None:
        run = self._runs.get(run_id)
        if run:
            run.detener_flag = True
            run.pausa.set()  # por si estaba en pausa, para que pueda salir del bucle

    def obtener_historial(self, run_id: str) -> list[dict]:
        run = self._runs.get(run_id)
        return run.historial if run else []

    async def ejecutar(self, run: Run, objetivo_arr: np.ndarray, enviar):
        """Corre el motor y envía un mensaje por generación usando `enviar` (coroutine)."""
        gen = evolucionar(
            run.params, objetivo_arr, debe_detener=lambda: run.detener_flag
        )
        try:
            while True:
                await run.pausa.wait()
                try:
                    estado: EstadoGeneracion = await gen.__anext__()
                except StopAsyncIteration:
                    break

                mejora = (
                    run.ultimo_mejor is None or estado.mejor_aptitud > run.ultimo_mejor
                )
                if mejora:
                    run.ultimo_mejor = estado.mejor_aptitud

                run.historial.append(
                    {
                        "generacion": estado.generacion,
                        "mejor": estado.mejor_aptitud,
                        "promedio": estado.aptitud_promedio,
                    }
                )

                mensaje = {
                    "tipo": "generacion",
                    "generacion": estado.generacion,
                    "mejor_aptitud": estado.mejor_aptitud,
                    "aptitud_promedio": estado.aptitud_promedio,
                    "aptitud_peor": estado.aptitud_peor,
                    "tiempo_ms": estado.tiempo_ms,
                    "generaciones_sin_mejora": estado.generaciones_sin_mejora,
                }
                if mejora:
                    mensaje["genoma_mejor"] = decodificar(estado.genoma_mejor)

                await enviar(mensaje)

                if estado.razon_parada is not None:
                    run.razon = estado.razon_parada
                    await enviar(
                        {
                            "tipo": "finalizado",
                            "razon": estado.razon_parada,
                            "generaciones": estado.generacion,
                        }
                    )
                    break
        finally:
            run.terminado = True
            await gen.aclose()
