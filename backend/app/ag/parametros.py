"""Parámetros de configuración del algoritmo genético (TSP)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ParametrosAG(BaseModel):
    poblacion: int = 60
    num_ciudades: int = 30
    origen_ciudades: str = "aleatorio"  # "aleatorio" | "metro_medellin"
    prob_cruce: float = 0.85
    prob_mutacion: float = 0.15
    elitismo: int = 3
    seleccion: str = "torneo"
    k_torneo: int = 3
    num_mejores: int = 10  # usado por selección "heuristica" (truncamiento)
    cruce: str = "dos_puntos"
    mutacion: str = "heuristica"
    criterio_parada: str = "generaciones"
    max_generaciones: int = 400
    epsilon: float = 0.0005
    paciencia: int = 40
    distancia_objetivo: float = 5.0
    semilla_ciudades: int | None = None
    seed: int | None = None

    model_config = ConfigDict(extra="forbid")
