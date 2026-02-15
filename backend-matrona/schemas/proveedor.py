from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
#from schemas.materiales import MaterialCreate

#esquema base
class ProveedorBase(BaseModel):
    nombre_proveedor: str
    material_que_provee: str
    cantidadM: str
    telefono: Optional[str] = None
    direccion_proveedor: Optional[str] = None
    frecuencia_entrega: Optional[str] = None

#enum para actividad
class ActividadEnum(str,Enum):
    producir = "producir"
    envasar = "envasar"

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

#modelo para vincular materiales
class MaterialInline(BaseModel):
    actividad: ActividadEnum
    tipo_material: str
    cantidad_disponible: Optional[str] = None
    cantidad_a_agregar: Optional[str] = None

#proveedor completo
class ProveedorMaterial(BaseModel):
    nombre_proveedor: str
    material_que_provee: str
    cantidadM: str
    telefono: Optional[str] = None
    direccion_proveedor: Optional[str] = None
    frecuencia_entrega: Optional[str] = None
    materiales: MaterialInline
    class Config:
        orm_mode = True


