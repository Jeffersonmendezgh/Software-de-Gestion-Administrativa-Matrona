from pydantic import BaseModel
from typing import Optional, List

#esquema base
class ProveedorBase(BaseModel):
    nombre_proveedor: str
    material_que_provee: str
    cantidadM: str
    telefono: Optional[str] = None
    direccion_proveedor: Optional[str] = None
    frecuencia_entrega: Optional[str] = None


# para mostrar proveedores
class ProveedorOut(ProveedorBase):
    id_proveedor: int
    class Config:
        orm_mode = True
        
# Este se usa para CREAR un proveedor
class ProveedorCreate(BaseModel):
    nombre_proveedor: str
    material_que_provee: str
    cantidadM: str
    telefono: Optional[str] = None
    direccion_proveedor: Optional[str] = None
    frecuencia_entrega: Optional[str] = None

#para modificar proveedor
class ProveedorModified(BaseModel):
    material_que_provee: str
    cantidadM: str
    telefono: Optional[str] = None
    direccion_proveedor: Optional[str] = None
    frecuencia_entrega: Optional[str] = None


