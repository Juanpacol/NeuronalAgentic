"""Parámetros iniciales del algoritmo genético (C5): optimización de dieta."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ParametrosAG(BaseModel):
    # --- población y operadores (genéricos del AG) ---
    poblacion: int = 80
    prob_cruce: float = 0.85
    prob_mutacion: float = 0.15
    elitismo: int = 3
    seleccion: str = "torneo"
    k_torneo: int = 3
    num_mejores: int = 10  # usado por selección "heuristica" (truncamiento)
    cruce: str = "dos_puntos"
    mutacion: str = "heuristica"

    # --- criterios de parada ---
    criterio_parada: str = "generaciones"
    max_generaciones: int = 400
    epsilon: float = 0.0005
    paciencia: int = 40
    aptitud_objetivo: float = 0.95

    # --- metas nutricionales del usuario (objetivo del problema) ---
    objetivo_kcal: float = 2000
    objetivo_proteina_g: float = 75
    objetivo_carbohidratos_g: float = 250
    objetivo_grasa_g: float = 65

    # --- costo ---
    # peso_costo=0.5: la nutrición es la restricción, el costo es el desempate
    # entre dietas nutricionalmente válidas. A 0.5, una dieta 20% sobre
    # presupuesto pesa lo mismo que estar 10% lejos de la meta de calorías.
    peso_costo: float = 0.5
    presupuesto_cop: float = 20000

    # --- ejecución ---
    seed: int | None = None
    # Si el AG converge más rápido de lo que se alcanza a ver en la demo, se
    # frena aquí en vez de inflar artificialmente la población.
    retardo_ms: int = 0

    model_config = ConfigDict(extra="forbid")
