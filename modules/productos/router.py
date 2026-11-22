from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from database.almacen import abrir_puerta
from modules.productos.schema import (
    Revisar_JSON_Crear_Producto, 
    Revisar_JSON_Editar_Producto,
    Revisar_JSON_Editar_Producto_Parcial,
    ProductoRespuesta
)
from core.schema import RespuestaPaginada
from modules.productos.service import ProductosService as service
from utils.auth import permiso_admin, permiso_usuario

router = APIRouter(
    prefix="/products",
    tags=["Productos"],
    dependencies=[Depends(permiso_usuario)]
)

@router.post(
    "/",
    response_model=ProductoRespuesta,
    status_code=status.HTTP_201_CREATED
)
def crear_nuevo_producto(
    json: Revisar_JSON_Crear_Producto, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_usuario)
):
    return service.crear_producto(db, json)

@router.get(
    "/",
    response_model=RespuestaPaginada[ProductoRespuesta],
    status_code=status.HTTP_200_OK
)
def obtener_productos(
    salto: int = Query(default=0, ge=0),
    # El maximo protege la base de datos de respuestas demasiado grandes.
    limite: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.obtener_productos_service(db, salto, limite)


@router.get(
    "/{id}",
    response_model=ProductoRespuesta,
    status_code=status.HTTP_200_OK
)
def obtener_producto(
    id: int = Path(ge=1),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_usuario)
):
    return service.obtener_producto_por_id(db, id)


@router.put("/{id}", response_model=ProductoRespuesta)
def editar(
    json: Revisar_JSON_Editar_Producto,
    id: int = Path(ge=1),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.editar_producto(db, json, id)

@router.patch("/{id}", response_model=ProductoRespuesta)
def editar_parcial(
    json: Revisar_JSON_Editar_Producto_Parcial,
    id: int = Path(ge=1),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.editar_producto_parcial(db, json, id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    id: int = Path(ge=1),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.eliminar_producto(db, id)
