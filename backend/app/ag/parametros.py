"""Parámetros de configuración del algoritmo genético."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ParametrosAG(BaseModel):
    poblacion: int = 40
    num_triangulos: int = 80
    prob_cruce: float = 0.7
    prob_mutacion: float = 0.15
    elitismo: int = 2
    seleccion: str = "torneo"
    k_torneo: int = 3
    num_mejores: int = 10  # usado por selección "heuristica" (truncamiento)
    cruce: str = "uniforme"
    cruce_por_triangulo: bool = False
    mutacion: str = "heuristica"
    sigma_mutacion: float = 0.1
    operador_reordenamiento: str | None = None
    prob_reordenamiento: float = 0.05
    criterio_parada: str = "generaciones"
    max_generaciones: int = 300
    epsilon: float = 0.0005
    paciencia: int = 30
    aptitud_objetivo: float = 0.97
    resolucion_trabajo: int = 128
    seed: int | None = None

    model_config = ConfigDict(extra="forbid")
