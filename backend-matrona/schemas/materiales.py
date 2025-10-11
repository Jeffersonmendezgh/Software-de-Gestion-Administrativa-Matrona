from pydantic import BaseModel
from typing import Optional
from schemas.proveedor import ProveedorOut

#esquema base
class MaterialBase(BaseModel):
    tipo_material: str
    cantidad_disponible: Optional[str] = None
    actividad: Optional[str] = None
    cantidad_a_agregar: Optional[str] = None
    id_proveedor: Optional[int] = None

#para crear
class MaterialCreate(MaterialBase):
    pass

#para mostar materiales
class MaterialesOut(MaterialBase):
    id_materiales: int
    proveedor: Optional[ProveedorOut] = None

    class Config:
        orm_mode = True

#mateial update
class MaterialUpdate(BaseModel):
    tipo_material: str
    cantidad_a_agregar: str

class MaterialResponse(MaterialBase):
    id_materiales: int

    class Config:
        orm_mode = True
