"""Registro central de operadores del algoritmo genético (nombre -> función)."""
from __future__ import annotations

from . import cruce, mutacion, seleccion

REGISTRO_SELECCION = {
    "proporcional": seleccion.proporcional,
    "torneo": seleccion.torneo,
    "estocastica": seleccion.estocastica,
    "heuristica": seleccion.heuristica,
}

REGISTRO_CRUCE = {
    "un_punto": cruce.un_punto,
    "dos_puntos": cruce.dos_puntos,
    "uniforme": cruce.uniforme,
}

REGISTRO_MUTACION = {
    "heuristica": mutacion.heuristica,
    "intercambio": mutacion.intercambio,
    "desplazamiento": mutacion.desplazamiento,
    "insercion": mutacion.insercion,
}


def nombres_disponibles() -> dict:
    """Devuelve los nombres de todas las técnicas disponibles, para el frontend."""
    return {
        "seleccion": sorted(REGISTRO_SELECCION.keys()),
        "cruce": sorted(REGISTRO_CRUCE.keys()),
        "mutacion": sorted(REGISTRO_MUTACION.keys()),
    }
