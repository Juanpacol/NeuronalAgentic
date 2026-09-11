"""Guardas sobre el catálogo: atrapan errores de transcripción de los datos ICBF."""
import numpy as np
import pytest

from app.ag.alimentos import (
    CATALOGO,
    CATEGORIAS,
    EXCEPCIONES_ATWATER,
    catalogo_serializable,
    construir_contexto,
)

CAMPOS_NUTRICIONALES = [
    "kcal_100g", "proteina_g_100g", "carbohidratos_g_100g", "grasa_g_100g",
]


def test_catalogo_tiene_25_alimentos():
    assert len(CATALOGO) == 25


def test_sin_valores_none():
    """Ningún dato puede quedar sin rellenar: un None silencioso rompería el fitness."""
    faltantes = []
    for a in CATALOGO:
        for campo in CAMPOS_NUTRICIONALES + ["gramos_porcion", "precio_cop", "max_porciones"]:
            if a.get(campo) is None:
                faltantes.append((a["nombre"], campo))
    assert faltantes == [], f"Valores sin rellenar: {faltantes}"


def test_todo_alimento_declara_codigo_tcac():
    """La trazabilidad a la tabla oficial es lo que hace auditable el conjunto."""
    for a in CATALOGO:
        assert a["codigo_tcac"], f"{a['nombre']} sin código TCAC"


def test_todo_precio_declara_si_esta_verificado():
    """Los precios son el dato débil: nadie debe confundir estimación con fuente."""
    for a in CATALOGO:
        assert isinstance(a["precio_verificado"], bool), a["nombre"]


@pytest.mark.parametrize("alimento", CATALOGO, ids=lambda a: a["codigo_tcac"])
def test_coherencia_atwater(alimento):
    """4*proteína + 4*carbohidratos + 9*grasa debe acercarse a las kcal declaradas.

    Es la red de seguridad contra errores de transcripción: si alguien copia mal
    una cifra de la TCAC, casi siempre rompe esta identidad.
    """
    if alimento["codigo_tcac"] in EXCEPCIONES_ATWATER:
        pytest.skip("excepción documentada: fibra alta desvía el cálculo de Atwater")

    estimado = (
        4 * alimento["proteina_g_100g"]
        + 4 * alimento["carbohidratos_g_100g"]
        + 9 * alimento["grasa_g_100g"]
    )
    declarado = alimento["kcal_100g"]
    if declarado == 0:
        return
    desviacion = abs(estimado - declarado) / declarado
    assert desviacion <= 0.15, (
        f"{alimento['nombre']}: Atwater {estimado:.1f} vs declarado {declarado} "
        f"({desviacion:.1%} de desviación)"
    )


def test_categorias_validas():
    for a in CATALOGO:
        assert a["categoria"] in CATEGORIAS


def test_valores_por_porcion_se_derivan_de_los_de_100g():
    """Los valores por porción se calculan, no se transcriben: no puede haber deriva."""
    serial = catalogo_serializable()
    for crudo, listo in zip(CATALOGO, serial):
        esperado = crudo["kcal_100g"] * crudo["gramos_porcion"] / 100.0
        assert listo["kcal"] == pytest.approx(esperado, abs=0.01)


def test_contexto_tiene_formas_coherentes():
    ctx = construir_contexto(2000, 75, 250, 65, 0.5, 20000)
    n = len(CATALOGO)
    assert ctx.matriz_nutrientes.shape == (n, 4)
    assert ctx.precios.shape == (n,)
    assert ctx.max_porciones.shape == (n,)
    assert ctx.objetivos.shape == (4,)
    assert ctx.pesos_macro.shape == (4,)
    assert ctx.pesos_macro.sum() == pytest.approx(1.0)
    assert ctx.num_alimentos == n


def test_indices_por_categoria_cubren_todos_los_alimentos():
    ctx = construir_contexto(2000, 75, 250, 65, 0.5, 20000)
    todos = np.concatenate(list(ctx.indices_por_categoria.values()))
    assert sorted(todos.tolist()) == list(range(ctx.num_alimentos))


def test_hay_al_menos_dos_alimentos_por_categoria():
    """El operador de intercambio necesita pares dentro de la misma categoría."""
    ctx = construir_contexto(2000, 75, 250, 65, 0.5, 20000)
    for cat, indices in ctx.indices_por_categoria.items():
        assert len(indices) >= 2, f"categoría {cat} con menos de 2 alimentos"
