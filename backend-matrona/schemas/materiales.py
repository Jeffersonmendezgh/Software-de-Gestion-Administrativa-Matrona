from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

#mateial update
class MaterialUpdate(BaseModel):
    tipo_material: str
    cantidad_a_agregar: str

class MaterialResponse(MaterialBase):
    id_materiales: int

    model_config = ConfigDict(from_attributes=True)
