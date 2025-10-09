from pydantic import BaseModel
from typing import Optional
from schemas.proveedor import ProveedorOut

#esquema base
class MateralesBase(BaseModel):
    tipo_material: str
    cantidad_disponible: Optional[str] = None
    cantidad_a_agregar: Optional[str] = None
    id_proveedor: int

#para crear
class MaterialesCreate(MateralesBase):
    pass

#para mostar materiales
class MaterialesOut(MateralesBase):
    id_materiales: int
    proveedor: Optional[ProveedorOut] = None

    class Config:
        orm_mode = True


