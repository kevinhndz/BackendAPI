def test_crear_producto(cliente):
    respuesta = cliente.post(
        "/products/",
        json={
            "nombre": "Teclado mecanico",
            "stock": 10,
            "codigo": "TEC-001"
        }
    )

    assert respuesta.status_code == 201
    assert respuesta.json() == {
        "id": 1,
        "nombre": "Teclado mecanico",
        "stock": 10,
        "codigo": "TEC-001"
    }


def test_crear_producto_rechaza_datos_invalidos(cliente):
    respuesta = cliente.post(
        "/products/",
        json={"nombre": "PC", "stock": -1, "codigo": "codigo invalido"}
    )

    assert respuesta.status_code == 422


def test_listar_productos_paginados(cliente, crear_producto):
    crear_producto(nombre="Producto uno", codigo="PRO-001")
    crear_producto(nombre="Producto dos", codigo="PRO-002")
    crear_producto(nombre="Producto tres", codigo="PRO-003")

    respuesta = cliente.get("/products/?salto=1&limite=1")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "total": 3,
        "pagina_actual": 2,
        "limite": 1,
        "total_paginas": 3,
        "data": [
            {
                "id": 2,
                "nombre": "Producto dos",
                "stock": 10,
                "codigo": "PRO-002"
            }
        ]
    }


def test_listar_productos_devuelve_lista_vacia(cliente):
    respuesta = cliente.get("/products/")

    assert respuesta.status_code == 200
    assert respuesta.json()["total"] == 0
    assert respuesta.json()["data"] == []


def test_listar_productos_rechaza_limite_mayor_a_cien(cliente):
    respuesta = cliente.get("/products/?limite=101")

    assert respuesta.status_code == 422


def test_obtener_producto_por_id(cliente, crear_producto):
    producto = crear_producto()

    respuesta = cliente.get(f"/products/{producto['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == producto


def test_obtener_producto_inexistente(cliente):
    respuesta = cliente.get("/products/999")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "No se encontro el recurso"


def test_editar_producto_completo(cliente, crear_producto):
    producto = crear_producto()

    respuesta = cliente.put(
        f"/products/{producto['id']}",
        json={
            "nombre": "Teclado actualizado",
            "stock": 25,
            "codigo": "TEC-002"
        }
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Teclado actualizado"
    assert respuesta.json()["stock"] == 25
    assert respuesta.json()["codigo"] == "TEC-002"


def test_editar_producto_parcial(cliente, crear_producto):
    producto = crear_producto()

    respuesta = cliente.patch(
        f"/products/{producto['id']}",
        json={"stock": 50}
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == producto["nombre"]
    assert respuesta.json()["stock"] == 50


def test_editar_producto_parcial_rechaza_cuerpo_vacio(cliente, crear_producto):
    producto = crear_producto()

    respuesta = cliente.patch(f"/products/{producto['id']}", json={})

    assert respuesta.status_code == 422


def test_editar_producto_parcial_rechaza_valor_nulo(cliente, crear_producto):
    producto = crear_producto()

    respuesta = cliente.patch(
        f"/products/{producto['id']}",
        json={"nombre": None}
    )

    assert respuesta.status_code == 422


def test_eliminar_producto(cliente, crear_producto):
    producto = crear_producto()

    respuesta = cliente.delete(f"/products/{producto['id']}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""
    assert cliente.get(f"/products/{producto['id']}").status_code == 404


def test_eliminar_producto_inexistente(cliente):
    respuesta = cliente.delete("/products/999")

    assert respuesta.status_code == 404
