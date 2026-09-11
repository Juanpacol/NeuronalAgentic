"""Criterios de parada del algoritmo genético."""
from __future__ import annotations

from .parametros import ParametrosAG


def evaluar_parada(
    params: ParametrosAG,
    generacion: int,
    aptitud_mejor: float,
    generaciones_sin_mejora: int,
    detener_externo: bool = False,
) -> str | None:
    """Devuelve la razón de parada si corresponde, o None si se debe continuar."""
    if detener_externo:
        return "detenido_por_usuario"

    if params.criterio_parada == "objetivo":
        # OJO CON LA DIRECCIÓN: en este dominio MAYOR aptitud es mejor, así que
        # se para al ALCANZAR o superar el objetivo. En el dominio anterior
        # (TSP) la métrica era distancia y la comparación iba al revés.
        if aptitud_mejor >= params.aptitud_objetivo:
            return "aptitud_objetivo_alcanzada"
        if generacion >= params.max_generaciones:
            return "max_generaciones"
        return None

    if params.criterio_parada == "convergencia":
        if generaciones_sin_mejora >= params.paciencia:
            return "convergencia"
        if generacion >= params.max_generaciones:
            return "max_generaciones"
        return None

    # criterio_parada == "generaciones" (default)
    if generacion >= params.max_generaciones:
        return "max_generaciones"
    return None
