from pydantic import BaseModel
from typing import Optional
from datetime import date

#Base para lectura de usuario
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: Optional[str] = None
    direccion: Optional[str] = None
    class Config:
        orm_mode = True

class EmpleadoBase(BaseModel):
    fecha_contratacion: Optional[date] = None
    salario: Optional[float] = None
    fecha_pago: Optional[date] = None
    area_laboral: Optional[str] = None
    telefono_empleado: Optional[str] = None

class EmpleadoCreate(EmpleadoBase):
    id_usuarios: int
#actualizar empleado
class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_contratacion: Optional[date] = None
    salario: Optional[float] = None
    fecha_pago: Optional[date] = None
    area_laboral: Optional[str] = None
    telefono_empleado: Optional[str] = None
#respuesta de empleado
class EmpleadoResponse(EmpleadoBase):
    id_empleado: int
    fecha_contratacion: Optional[date]
    salario: Optional[float]
    fecha_pago: Optional[date]
    area_laboral: Optional[str]
    telefono_empleado: Optional[str]
    usuario: UsuarioBase
    

    class Config:
        orm_mode = True

