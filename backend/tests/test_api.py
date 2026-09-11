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
    assert data["defaults"]["poblacion"] > 0


def test_listar_targets():
    resp = client.get("/api/targets")
    assert resp.status_code == 200
    data = resp.json()
    assert any(t["id"] == "default" for t in data)


def test_websocket_evolucion_corrida_corta():
    with client.websocket_connect("/ws/evolucion") as ws:
        ws.send_json({
            "tipo": "iniciar",
            "params": {
                "poblacion": 6,
                "num_triangulos": 5,
                "max_generaciones": 3,
                "resolucion_trabajo": 32,
                "seed": 1,
            },
            "target_id": "default",
        })

        tipos = []
        primero = ws.receive_json()
        assert primero["tipo"] == "iniciado"
        assert "run_id" in primero
        tipos.append(primero["tipo"])

        while True:
            mensaje = ws.receive_json()
            tipos.append(mensaje["tipo"])
            if mensaje["tipo"] == "finalizado":
                assert mensaje["razon"] == "max_generaciones"
                break

        assert tipos[0] == "iniciado"
        assert "generacion" in tipos
        assert tipos[-1] == "finalizado"


def test_historial_de_corrida():
    with client.websocket_connect("/ws/evolucion") as ws:
        ws.send_json({
            "tipo": "iniciar",
            "params": {
                "poblacion": 6,
                "num_triangulos": 5,
                "max_generaciones": 2,
                "resolucion_trabajo": 32,
                "seed": 1,
            },
            "target_id": "default",
        })
        primero = ws.receive_json()
        run_id = primero["run_id"]
        while True:
            mensaje = ws.receive_json()
            if mensaje["tipo"] == "finalizado":
                break

    resp = client.get(f"/api/runs/{run_id}/historial")
    assert resp.status_code == 200
    historial = resp.json()
    assert len(historial) >= 1
    assert "generacion" in historial[0]
    assert "mejor" in historial[0]
    assert "promedio" in historial[0]
