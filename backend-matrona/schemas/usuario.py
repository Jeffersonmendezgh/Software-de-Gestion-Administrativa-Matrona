# schemas.py
from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    id_usuarios: int
    id_rol: Optional[int]
    nombre: str
    apellido: str
    correo: str
    direccion: Optional[str]

    class Config:
        orm_mode = True
#de aca para abajo va el post
class UsuarioCreate(BaseModel):
    id_rol: Optional[int]
    nombre: str
    apellido: str
    correo: str
    contrasena: str   # ⚠️ nombre en Python (mapeará a "contraseña" en MySQL)
    direccion: Optional[str]

#PUT
class UsuarioPut(BaseModel):
    id_rol: int
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    direccion: str

    class Config:
        orm_mode = True