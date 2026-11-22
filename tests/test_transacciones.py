import pytest

from core.exceptions import RecursoDuplicadoError
from modules.productos.model import Productos
from modules.productos.repository import ProductosRepository as repo
from modules.productos.schema import Revisar_JSON_Crear_Producto
from modules.productos.service import ProductosService as service


def test_rollback_permite_reutilizar_la_sesion(sesion_pruebas, monkeypatch):
    producto_guardado = Productos(
        nombre="Producto original",
        stock=10,
        codigo="REP-001"
    )
    sesion_pruebas.add(producto_guardado)
    sesion_pruebas.commit()

    # Simula dos peticiones que revisaron el codigo antes de guardar.
    monkeypatch.setattr(
        repo,
        "revisar_duplicados_codigo",
        lambda db, codigo: None
    )

    producto_repetido = Revisar_JSON_Crear_Producto(
        nombre="Producto repetido",
        stock=5,
        codigo="REP-001"
    )

    with pytest.raises(RecursoDuplicadoError):
        service.crear_producto(sesion_pruebas, producto_repetido)

    # La misma sesion puede consultar porque el service ejecuto rollback.
    total_productos = sesion_pruebas.query(Productos).count()
    assert total_productos == 1
