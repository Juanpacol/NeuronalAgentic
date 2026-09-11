from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_opciones_parametros():
    resp = client.get("/api/parametros/opciones")
    assert resp.status_code == 200
    data = resp.json()
    assert "seleccion" in data
    assert "cruce" in data
    assert "mutacion" in data
    assert "defaults" in data
    assert "torneo" in data["seleccion"]
    # metas del dominio de dieta, no restos del dominio anterior
    assert data["defaults"]["objetivo_kcal"] > 0
    assert data["defaults"]["presupuesto_cop"] > 0
    for residuo in ("num_ciudades", "origen_ciudades", "distancia_objetivo", "num_triangulos"):
        assert residuo not in data["defaults"], f"quedó un parámetro del dominio anterior: {residuo}"


def test_websocket_corrida_corta():
    with client.websocket_connect("/ws/evolucion") as ws:
        ws.send_json({
            "tipo": "iniciar",
            "params": {
                "poblacion": 20,
                "max_generaciones": 5,
                "criterio_parada": "generaciones",
                "seed": 1,
            },
        })

        msg = ws.receive_json()
        assert msg["tipo"] == "iniciado"
        assert len(msg["alimentos"]) == 25
        assert {"kcal", "proteina_g", "carbohidratos_g", "grasa_g", "presupuesto_cop"} <= set(
            msg["objetivos"]
        )
        primero = msg["alimentos"][0]
        for campo in ("nombre", "categoria", "unidad", "kcal", "precio_cop", "max_porciones"):
            assert campo in primero

        tipos = []
        vio_genoma = False
        while True:
            msg = ws.receive_json()
            tipos.append(msg["tipo"])
            if msg["tipo"] == "generacion":
                for campo in ("mejor_aptitud", "costo_mejor", "macros_mejor",
                              "pen_macro", "pen_costo", "aptitudes"):
                    assert campo in msg
                assert len(msg["aptitudes"]) == 20
                if "genoma_mejor" in msg:
                    vio_genoma = True
                    assert len(msg["genoma_mejor"]) == 25
            if msg["tipo"] == "finalizado":
                assert msg["generaciones"] == 5
                break

        assert tipos.count("generacion") >= 1
        assert tipos[-1] == "finalizado"
        assert vio_genoma, "nunca se envió el genoma del mejor individuo"


def test_historial_corrida_inexistente():
    resp = client.get("/api/runs/no-existe/historial")
    assert resp.status_code == 404
