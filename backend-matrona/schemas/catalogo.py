from pydantic import BaseModel
from typing import Optional


# Mini esquema de Inventario (solo info necesaria)
class InventarioMini(BaseModel):
    id_inventario: int
    nombre_bebida: str
    cantidad_disponible: int

    class Config:
        orm_mode = True


# Esquema base de Catálogo (lo que se devuelve al frontend)
class CatalogoBase(BaseModel):
    id_catalogo: int
    id_inventario: int
    descripcion: Optional[str]
    contenido: Optional[int]
    alcohol: Optional[str]
    precio_unidad: Optional[float]
    precio_sixpack: Optional[float]
    precio_caja: Optional[float]

    # Relación para mostrar también inventario
    inventario: Optional[InventarioMini]

    class Config:
        orm_mode = True


# Esquema para crear catálogo + inventario juntos
class CatalogoCreate(BaseModel):
    nombre_bebida: str
    cantidad_disponible: int  # viene del form
    descripcion: Optional[str]
    alcohol: Optional[str]
    contenido: Optional[int] 
    precio_unidad: Optional[float]
    precio_sixpack: Optional[float]
    precio_caja: Optional[float]