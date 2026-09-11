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
    assert data["defaults"]["num_ciudades"] > 0


def test_websocket_corrida_corta():
    with client.websocket_connect("/ws/evolucion") as ws:
        ws.send_json({
            "tipo": "iniciar",
            "params": {
                "poblacion": 10,
                "num_ciudades": 6,
                "max_generaciones": 5,
                "criterio_parada": "generaciones",
            },
        })

        msg = ws.receive_json()
        assert msg["tipo"] == "iniciado"
        assert len(msg["ciudades"]) == 6

        tipos_recibidos = []
        while True:
            msg = ws.receive_json()
            tipos_recibidos.append(msg["tipo"])
            if msg["tipo"] == "finalizado":
                assert msg["generaciones"] == 5
                break

        assert tipos_recibidos.count("generacion") >= 1
        assert tipos_recibidos[-1] == "finalizado"


def test_historial_corrida_inexistente():
    resp = client.get("/api/runs/no-existe/historial")
    assert resp.status_code == 404
