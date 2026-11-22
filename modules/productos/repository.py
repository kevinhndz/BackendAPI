import math
from sqlalchemy.orm import Session
from modules.productos.model import Productos

class ProductosRepository():
    
    @staticmethod
    def revisar_duplicados_codigo(db: Session, codigo: str) -> dict:
        check = db.query(Productos).filter(Productos.codigo == codigo).first()
        return check
        
    @staticmethod
    def crear_nuevo_producto(db: Session, new_product: Productos) -> Productos:
        db.add(new_product)
        # flush envia la operacion a la base sin confirmar la transaccion.
        db.flush()
        return new_product

    @staticmethod
    def obtener_productos(db: Session, salto: int, limite: int):
        total_registros = db.query(Productos).count()
        productos = (
            db.query(Productos)
            # El orden por id evita que un producto cambie de pagina entre consultas.
            .order_by(Productos.id)
            .offset(salto)
            .limit(limite)
            .all()
        )
        
        pagina_actual = (salto // limite) + 1
        total_paginas = math.ceil(total_registros / limite) if total_registros > 0 else 1
        
        return {
            "total": total_registros,
            "pagina_actual": pagina_actual,
            "limite": limite,
            "total_paginas": total_paginas,
            "data": productos
        }

    @staticmethod
    def buscar_por_id(db: Session, id: int):
        return db.query(Productos).filter(Productos.id == id).first()
    
    @staticmethod
    def guardar_cambios_put(
        db: Session,
        producto_editado: Productos
    ) -> Productos:
        db.flush()
        return producto_editado

    @staticmethod
    def guardar_cambios_patch(db: Session, producto: Productos) -> Productos:
        db.flush()
        return producto

    @staticmethod
    def eliminar_producto(db: Session, producto: Productos) -> None:
        db.delete(producto)
        db.flush()
