from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional


class ProductoBase(BaseModel):
    # Rechaza campos desconocidos para detectar errores del cliente de inmediato.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    nombre: str = Field(min_length=3, max_length=25)
    stock: int = Field(ge=0)
    codigo: str = Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9-]+$")


class Revisar_JSON_Crear_Producto(ProductoBase):
    pass


class Revisar_JSON_Editar_Producto(ProductoBase):
    pass

class Revisar_JSON_Editar_Producto_Parcial(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    nombre: Optional[str] = Field(None, min_length=3, max_length=25)
    stock: Optional[int] = Field(None, ge=0)
    codigo: Optional[str] = Field(
        None,
        min_length=1,
        max_length=30,
        pattern=r"^[A-Za-z0-9-]+$"
    )

    @model_validator(mode="before")
    @classmethod
    def validar_campos_enviados(cls, datos):
        # Un PATCH vacio no representa ningun cambio y debe rechazarse.
        if not datos:
            raise ValueError("Debe enviar al menos un campo para actualizar")

        # La tabla no permite valores nulos en los campos del producto.
        if any(valor is None for valor in datos.values()):
            raise ValueError("Los campos enviados no pueden ser nulos")

        return datos
    
class ProductoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    stock: int
    codigo: str
