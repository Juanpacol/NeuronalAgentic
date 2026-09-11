"""Catálogo de alimentos (C2/C3): datos nutricionales y contexto del problema de dieta.

PROCEDENCIA DE LOS DATOS — leer antes de citar este archivo en el informe
------------------------------------------------------------------------
1. VALORES NUTRICIONALES: verificados. Provienen de la Tabla de Composición de
   Alimentos Colombianos (TCAC) del ICBF, 2ª edición 2018 (ICBF / Universidad
   Nacional de Colombia). Cada alimento conserva su código TCAC oficial en el
   campo `codigo_tcac`, de modo que cualquier valor se puede auditar contra la
   tabla original. Los valores están expresados por 100 g de parte comestible,
   tal como los publica la TCAC; los valores por porción se DERIVAN por cálculo
   (ver `_por_porcion`), nunca se transcriben a mano, para no introducir errores.

2. GRAMOS POR PORCIÓN: medidas caseras convencionales (taza, unidad, cucharada,
   tajada). NO provienen de la TCAC: son el tamaño de servicio con el que se
   presenta el problema al usuario. Se documentan como tales y no se presentan
   como dato oficial.

3. PRECIOS: NO VERIFICADOS. Son estimaciones de precio al detal en Medellín y
   están marcados individualmente con `precio_verificado = False`. Se intentó
   obtenerlos de DANE-SIPSA (boletines diario de 2026-07-10 y mensual de junio
   2026), pero SIPSA publica variaciones porcentuales y precios de coyuntura de
   unos pocos productos por jornada, no una tabla sistemática de precios
   absolutos para una canasta fija. La única excepción verificada es el tomate.
   ANTES DE PRESENTAR EL PROYECTO estos precios deberían reemplazarse por una
   captura real (factura de supermercado o consulta a la Central Mayorista de
   Antioquia), anotando el mes de captura.

   Mes de referencia de las estimaciones: septiembre de 2026.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

FUENTE_NUTRIENTES = "ICBF/UNAL, Tabla de Composición de Alimentos Colombianos (TCAC) 2018"
FUENTE_PRECIOS_ESTIMADOS = "Estimación de precio al detal en Medellín (sin verificar), sep-2026"
FUENTE_PRECIO_SIPSA_TOMATE = "DANE-SIPSA, Central Mayorista de Antioquia, may-2026 ($1.413/kg)"

CATEGORIAS = ["carbohidratos", "proteinas", "verduras_frutas", "grasas_otros"]

# Orden de los macronutrientes en todas las matrices y vectores del módulo.
MACROS = ["kcal", "proteina_g", "carbohidratos_g", "grasa_g"]

# Alimentos con desviación de Atwater legítimamente alta (ver test_alimentos.py).
# La fibra se contabiliza dentro de los carbohidratos totales pero aporta menos
# energía que 4 kcal/g, así que las verduras de hoja se salen del margen sin que
# eso signifique un error de transcripción.
EXCEPCIONES_ATWATER = {"B043"}

CATALOGO: list[dict] = [
    # ---------------------------- carbohidratos ----------------------------
    {
        "codigo_tcac": "A009", "nombre": "Arroz blanco cocido", "categoria": "carbohidratos",
        "unidad": "taza", "gramos_porcion": 158,
        "kcal_100g": 161.0, "proteina_g_100g": 2.3, "carbohidratos_g_100g": 32.5, "grasa_g_100g": 2.1,
        "precio_cop": 711, "precio_verificado": False, "max_porciones": 4,
    },
    {
        "codigo_tcac": "A005", "nombre": "Arepa de maíz", "categoria": "carbohidratos",
        "unidad": "unidad", "gramos_porcion": 70,
        "kcal_100g": 156.0, "proteina_g_100g": 3.4, "carbohidratos_g_100g": 34.5, "grasa_g_100g": 0.5,
        "precio_cop": 500, "precio_verificado": False, "max_porciones": 4,
    },
    {
        "codigo_tcac": "B070", "nombre": "Papa criolla cocida", "categoria": "carbohidratos",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 85.0, "proteina_g_100g": 1.4, "carbohidratos_g_100g": 18.1, "grasa_g_100g": 0.0,
        "precio_cop": 400, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "B106", "nombre": "Yuca cocida", "categoria": "carbohidratos",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 157.0, "proteina_g_100g": 0.7, "carbohidratos_g_100g": 36.6, "grasa_g_100g": 0.2,
        "precio_cop": 250, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "B088", "nombre": "Plátano maduro cocido", "categoria": "carbohidratos",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 130.0, "proteina_g_100g": 0.8, "carbohidratos_g_100g": 30.1, "grasa_g_100g": 0.2,
        "precio_cop": 280, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "A060", "nombre": "Pan blanco", "categoria": "carbohidratos",
        "unidad": "tajada", "gramos_porcion": 30,
        "kcal_100g": 268.0, "proteina_g_100g": 8.9, "carbohidratos_g_100g": 48.8, "grasa_g_100g": 3.4,
        "precio_cop": 300, "precio_verificado": False, "max_porciones": 4,
    },
    {
        "codigo_tcac": "A012", "nombre": "Avena en hojuelas", "categoria": "carbohidratos",
        "unidad": "porción", "gramos_porcion": 40,
        "kcal_100g": 411.0, "proteina_g_100g": 16.9, "carbohidratos_g_100g": 64.1, "grasa_g_100g": 7.5,
        "precio_cop": 240, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "A073", "nombre": "Pasta cocida", "categoria": "carbohidratos",
        "unidad": "taza", "gramos_porcion": 140,
        "kcal_100g": 143.0, "proteina_g_100g": 5.8, "carbohidratos_g_100g": 27.0, "grasa_g_100g": 0.9,
        "precio_cop": 210, "precio_verificado": False, "max_porciones": 3,
    },
    # ------------------------------ proteínas ------------------------------
    {
        "codigo_tcac": "J003", "nombre": "Huevo cocido", "categoria": "proteinas",
        "unidad": "unidad", "gramos_porcion": 50,
        "kcal_100g": 145.0, "proteina_g_100g": 13.0, "carbohidratos_g_100g": 0.0, "grasa_g_100g": 10.4,
        "precio_cop": 550, "precio_verificado": False, "max_porciones": 4,
    },
    {
        "codigo_tcac": "F087", "nombre": "Pechuga de pollo cocida", "categoria": "proteinas",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 141.0, "proteina_g_100g": 28.4, "carbohidratos_g_100g": 0.3, "grasa_g_100g": 3.0,
        "precio_cop": 1600, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "F101", "nombre": "Carne de res molida", "categoria": "proteinas",
        "unidad": "porción", "gramos_porcion": 100,
        "kcal_100g": 194.0, "proteina_g_100g": 19.6, "carbohidratos_g_100g": 0.2, "grasa_g_100g": 12.7,
        "precio_cop": 2000, "precio_verificado": False, "max_porciones": 2,
    },
    {
        "codigo_tcac": "E004", "nombre": "Atún enlatado en agua", "categoria": "proteinas",
        "unidad": "lata", "gramos_porcion": 80,
        "kcal_100g": 127.0, "proteina_g_100g": 24.2, "carbohidratos_g_100g": 0.9, "grasa_g_100g": 3.0,
        "precio_cop": 4000, "precio_verificado": False, "max_porciones": 2,
    },
    {
        "codigo_tcac": "T010", "nombre": "Frijol cargamanto cocido", "categoria": "proteinas",
        "unidad": "taza", "gramos_porcion": 150,
        "kcal_100g": 161.0, "proteina_g_100g": 8.1, "carbohidratos_g_100g": 26.9, "grasa_g_100g": 0.6,
        "precio_cop": 440, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "T025", "nombre": "Lenteja cocida", "categoria": "proteinas",
        "unidad": "taza", "gramos_porcion": 150,
        "kcal_100g": 122.0, "proteina_g_100g": 7.7, "carbohidratos_g_100g": 18.5, "grasa_g_100g": 0.5,
        "precio_cop": 275, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "G017", "nombre": "Queso campesino", "categoria": "proteinas",
        "unidad": "tajada", "gramos_porcion": 30,
        "kcal_100g": 301.0, "proteina_g_100g": 17.5, "carbohidratos_g_100g": 0.3, "grasa_g_100g": 25.5,
        "precio_cop": 540, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "G012", "nombre": "Leche entera", "categoria": "proteinas",
        "unidad": "vaso", "gramos_porcion": 200,
        "kcal_100g": 55.0, "proteina_g_100g": 3.2, "carbohidratos_g_100g": 3.4, "grasa_g_100g": 3.2,
        "precio_cop": 760, "precio_verificado": False, "max_porciones": 3,
    },
    # --------------------------- verduras y frutas --------------------------
    {
        "codigo_tcac": "B103", "nombre": "Tomate", "categoria": "verduras_frutas",
        "unidad": "unidad", "gramos_porcion": 100,
        "kcal_100g": 23.0, "proteina_g_100g": 0.9, "carbohidratos_g_100g": 4.1, "grasa_g_100g": 0.1,
        "precio_cop": 141, "precio_verificado": True, "max_porciones": 3,
    },
    {
        "codigo_tcac": "B027", "nombre": "Cebolla cabezona", "categoria": "verduras_frutas",
        "unidad": "media unidad", "gramos_porcion": 50,
        "kcal_100g": 40.0, "proteina_g_100g": 1.4, "carbohidratos_g_100g": 7.7, "grasa_g_100g": 0.1,
        "precio_cop": 160, "precio_verificado": False, "max_porciones": 2,
    },
    {
        "codigo_tcac": "B109", "nombre": "Zanahoria cocida", "categoria": "verduras_frutas",
        "unidad": "unidad", "gramos_porcion": 70,
        "kcal_100g": 43.0, "proteina_g_100g": 0.8, "carbohidratos_g_100g": 8.1, "grasa_g_100g": 0.2,
        "precio_cop": 175, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "B043", "nombre": "Espinaca cocida", "categoria": "verduras_frutas",
        "unidad": "porción", "gramos_porcion": 80,
        "kcal_100g": 35.0, "proteina_g_100g": 2.9, "carbohidratos_g_100g": 4.1, "grasa_g_100g": 0.1,
        "precio_cop": 480, "precio_verificado": False, "max_porciones": 2,
    },
    {
        "codigo_tcac": "C010", "nombre": "Banano", "categoria": "verduras_frutas",
        "unidad": "unidad", "gramos_porcion": 100,
        "kcal_100g": 101.0, "proteina_g_100g": 1.5, "carbohidratos_g_100g": 22.3, "grasa_g_100g": 0.1,
        "precio_cop": 250, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "C062", "nombre": "Naranja", "categoria": "verduras_frutas",
        "unidad": "unidad", "gramos_porcion": 130,
        "kcal_100g": 41.0, "proteina_g_100g": 0.7, "carbohidratos_g_100g": 8.8, "grasa_g_100g": 0.3,
        "precio_cop": 364, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "C001", "nombre": "Aguacate Hass", "categoria": "verduras_frutas",
        "unidad": "media unidad", "gramos_porcion": 70,
        "kcal_100g": 221.0, "proteina_g_100g": 1.3, "carbohidratos_g_100g": 13.5, "grasa_g_100g": 16.4,
        "precio_cop": 560, "precio_verificado": False, "max_porciones": 2,
    },
    # ----------------------------- grasas y otros ----------------------------
    {
        "codigo_tcac": "D004", "nombre": "Aceite de girasol", "categoria": "grasas_otros",
        "unidad": "cucharada", "gramos_porcion": 14,
        "kcal_100g": 900.0, "proteina_g_100g": 0.0, "carbohidratos_g_100g": 0.0, "grasa_g_100g": 100.0,
        "precio_cop": 180, "precio_verificado": False, "max_porciones": 3,
    },
    {
        "codigo_tcac": "K033", "nombre": "Panela", "categoria": "grasas_otros",
        "unidad": "cucharada", "gramos_porcion": 20,
        "kcal_100g": 364.0, "proteina_g_100g": 0.6, "carbohidratos_g_100g": 90.2, "grasa_g_100g": 0.1,
        "precio_cop": 100, "precio_verificado": False, "max_porciones": 3,
    },
]


def _por_porcion(alimento: dict, campo_100g: str) -> float:
    """Deriva el valor por porción desde el valor por 100 g de la TCAC.

    Se calcula en vez de transcribirse para que no exista una segunda copia
    de los datos que pueda desincronizarse de la fuente oficial.
    """
    return alimento[campo_100g] * alimento["gramos_porcion"] / 100.0


def catalogo_serializable() -> list[dict]:
    """Catálogo con los valores por porción ya calculados, para la API y el frontend."""
    salida = []
    for a in CATALOGO:
        salida.append({
            "codigo_tcac": a["codigo_tcac"],
            "nombre": a["nombre"],
            "categoria": a["categoria"],
            "unidad": a["unidad"],
            "gramos_porcion": a["gramos_porcion"],
            "kcal": round(_por_porcion(a, "kcal_100g"), 2),
            "proteina_g": round(_por_porcion(a, "proteina_g_100g"), 2),
            "carbohidratos_g": round(_por_porcion(a, "carbohidratos_g_100g"), 2),
            "grasa_g": round(_por_porcion(a, "grasa_g_100g"), 2),
            "precio_cop": a["precio_cop"],
            "precio_verificado": a["precio_verificado"],
            "max_porciones": a["max_porciones"],
            "fuente": FUENTE_NUTRIENTES + f" (código {a['codigo_tcac']})",
        })
    return salida


@dataclass(frozen=True)
class ContextoDieta:
    """Todo lo que el motor necesita saber del problema, en forma vectorizada.

    Reemplaza a `matriz_distancias` del dominio anterior (TSP): es el objeto de
    contexto que se pasa a fitness y mutación a través de `motor.py`.
    """

    nombres: list[str]
    categorias: np.ndarray                 # int8 (n,) id de categoría
    indices_por_categoria: dict[int, np.ndarray]
    matriz_nutrientes: np.ndarray          # float64 (n, 4) por porción
    precios: np.ndarray                    # float64 (n,) COP por porción
    max_porciones: np.ndarray              # int32 (n,)
    objetivos: np.ndarray                  # float64 (4,)
    pesos_macro: np.ndarray                # float64 (4,) ya normalizados
    peso_costo: float
    presupuesto: float

    @property
    def num_alimentos(self) -> int:
        return len(self.nombres)

    # El cromosoma se define en bloques para poder añadir después un bloque de
    # ejercicios sin rediseñar: creación, mutación y recorte iteran sobre los
    # arrays de cotas en vez de asumir un único tipo de gen.
    @property
    def bloques(self) -> dict[str, slice]:
        return {"alimentos": slice(0, self.num_alimentos)}


def construir_contexto(
    objetivo_kcal: float,
    objetivo_proteina_g: float,
    objetivo_carbohidratos_g: float,
    objetivo_grasa_g: float,
    peso_costo: float,
    presupuesto_cop: float,
    catalogo: list[dict] | None = None,
) -> ContextoDieta:
    """Compila el catálogo y las metas del usuario en un ContextoDieta."""
    catalogo = catalogo if catalogo is not None else CATALOGO

    nombres = [a["nombre"] for a in catalogo]
    categorias = np.array([CATEGORIAS.index(a["categoria"]) for a in catalogo], dtype=np.int8)
    indices_por_categoria = {
        c: np.where(categorias == c)[0] for c in np.unique(categorias)
    }

    matriz_nutrientes = np.array(
        [[_por_porcion(a, f"{m}_100g") for m in MACROS] for a in catalogo],
        dtype=np.float64,
    )
    precios = np.array([a["precio_cop"] for a in catalogo], dtype=np.float64)
    max_porciones = np.array([a["max_porciones"] for a in catalogo], dtype=np.int32)

    objetivos = np.array(
        [objetivo_kcal, objetivo_proteina_g, objetivo_carbohidratos_g, objetivo_grasa_g],
        dtype=np.float64,
    )

    # Calorías y proteína pesan más que carbohidratos y grasa: son la restricción
    # que define la dieta. Se normalizan para que pen_macro quede en una escala
    # comparable con pen_costo (ambos son error relativo adimensional).
    pesos_macro = np.array([1.0, 1.0, 0.8, 0.8], dtype=np.float64)
    pesos_macro = pesos_macro / pesos_macro.sum()

    return ContextoDieta(
        nombres=nombres,
        categorias=categorias,
        indices_por_categoria={int(k): v for k, v in indices_por_categoria.items()},
        matriz_nutrientes=matriz_nutrientes,
        precios=precios,
        max_porciones=max_porciones,
        objetivos=objetivos,
        pesos_macro=pesos_macro,
        peso_costo=float(peso_costo),
        presupuesto=float(presupuesto_cop),
    )


def contexto_desde_parametros(params) -> ContextoDieta:
    """Atajo: construye el contexto desde un ParametrosAG."""
    return construir_contexto(
        objetivo_kcal=params.objetivo_kcal,
        objetivo_proteina_g=params.objetivo_proteina_g,
        objetivo_carbohidratos_g=params.objetivo_carbohidratos_g,
        objetivo_grasa_g=params.objetivo_grasa_g,
        peso_costo=params.peso_costo,
        presupuesto_cop=params.presupuesto_cop,
    )
