import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Estas variables permiten importar la aplicacion sin usar secretos reales.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "clave-exclusiva-para-pruebas")

from database.almacen import abrir_puerta, miclaseBase
from main import app
from utils.auth import permiso_admin, permiso_usuario


motor_pruebas = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    # StaticPool conserva la misma base en memoria durante toda la prueba.
    poolclass=StaticPool
)
SesionPruebas = sessionmaker(
    bind=motor_pruebas,
    autoflush=False,
    expire_on_commit=False
)


def abrir_bd_pruebas():
    db = SesionPruebas()
    try:
        yield db
    finally:
        db.close()


def usuario_permitido():
    # La autenticacion tiene sus propias pruebas y aqui se aisla el CRUD.
    return {"id_user": 1, "user": "pruebas", "rol": "Admin"}


app.dependency_overrides[abrir_puerta] = abrir_bd_pruebas
app.dependency_overrides[permiso_usuario] = usuario_permitido
app.dependency_overrides[permiso_admin] = usuario_permitido


@pytest.fixture(autouse=True)
def preparar_base_de_datos():
    # Cada prueba comienza vacia para que sus resultados sean repetibles.
    miclaseBase.metadata.drop_all(bind=motor_pruebas)
    miclaseBase.metadata.create_all(bind=motor_pruebas)
    yield


@pytest.fixture
def cliente():
    with TestClient(app) as robot:
        yield robot


@pytest.fixture
def sesion_pruebas():
    db = SesionPruebas()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def crear_producto(cliente):
    def crear(
        nombre="Teclado mecanico",
        stock=10,
        codigo="TEC-001"
    ):
        respuesta = cliente.post(
            "/products/",
            json={"nombre": nombre, "stock": stock, "codigo": codigo}
        )
        assert respuesta.status_code == 201
        return respuesta.json()

    return crear
