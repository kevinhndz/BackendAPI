def test_comprobar_estado_de_la_api(cliente):
    respuesta = cliente.get("/api/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}
