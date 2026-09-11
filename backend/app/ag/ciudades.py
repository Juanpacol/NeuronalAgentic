"""Generación del mapa de ciudades y su matriz de distancias."""
from __future__ import annotations

import numpy as np


def generar_ciudades(num_ciudades: int, seed: int | None) -> np.ndarray:
    """Genera coordenadas (num_ciudades, 2) en [0,1], con su propio rng sembrado."""
    rng = np.random.default_rng(seed)
    return rng.random((num_ciudades, 2))


def calcular_matriz_distancias(ciudades: np.ndarray) -> np.ndarray:
    """Matriz (n,n) de distancias euclidianas, vectorizada por broadcasting."""
    diff = ciudades[:, None, :] - ciudades[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


# Estaciones reales del Metro de Medellín (Línea A + Línea B), (nombre, lat, lon).
# Coordenadas tomadas de los infobox de Wikipedia de cada estación (WGS84).
ESTACIONES_METRO_MEDELLIN: list[tuple[str, float, float]] = [
    # Línea A (norte a sur)
    ("Niquía", 6.33778, -75.54444),
    ("Bello", 6.33028, -75.55361),
    ("Madera", 6.31583, -75.55542),
    ("Acevedo", 6.30028, -75.55847),
    ("Tricentenario", 6.29040, -75.56470),
    ("Caribe", 6.27833, -75.56944),
    ("Universidad", 6.26944, -75.56583),
    ("Hospital", 6.26389, -75.56333),
    ("Prado", 6.25694, -75.56611),
    ("Parque Berrío", 6.25028, -75.56833),
    ("San Antonio", 6.24722, -75.56972),
    ("Alpujarra", 6.24306, -75.57139),
    ("Exposiciones", 6.23861, -75.57306),
    ("Industriales", 6.23000, -75.57556),
    ("Poblado", 6.21222, -75.57806),
    ("Aguacatala", 6.19417, -75.58167),
    ("Ayurá", 6.18611, -75.58611),
    ("Envigado", 6.17472, -75.59694),
    ("Itagüí", 6.16294, -75.60671),
    ("Sabaneta", 6.15778, -75.61611),
    ("La Estrella", 6.15267, -75.62656),
    # Línea B (San Antonio a San Javier; San Antonio ya está en Línea A)
    ("Cisneros", 6.24917, -75.57528),
    ("Suramericana", 6.25306, -75.58306),
    ("Estadio", 6.25333, -75.58833),
    ("Floresta", 6.25861, -75.59778),
    ("Santa Lucía", 6.25806, -75.60375),
    ("San Javier", 6.25694, -75.61389),
]


def nombres_metro_medellin() -> list[str]:
    return [nombre for nombre, _, _ in ESTACIONES_METRO_MEDELLIN]


def generar_mapa_metro_medellin() -> np.ndarray:
    """Coordenadas reales del Metro de Medellín, proyectadas y normalizadas a [0,1]^2
    preservando la proporción real (no se distorsiona el mapa como un cuadrado)."""
    coords = np.array([(lon, -lat) for _, lat, lon in ESTACIONES_METRO_MEDELLIN])
    minimo = coords.min(axis=0)
    maximo = coords.max(axis=0)
    escala = float((maximo - minimo).max())
    normalizado = (coords - minimo) / escala
    # centra el eje más corto dentro del cuadrado [0,1]^2
    ancho, alto = (maximo - minimo) / escala
    normalizado[:, 0] += (1 - ancho) / 2
    normalizado[:, 1] += (1 - alto) / 2
    return normalizado
