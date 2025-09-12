# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    id_usuarios: int
    id_rol: Optional[int] = None
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
    contrasena: str   # 
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

class UsuarioOut(BaseModel):
    id_usuarios: int
    nombre: str
    apellido: Optional[str]
    correo: EmailStr 
    direccion: Optional[str] = None
    id_rol: Optional[int]

    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class Token(BaseModel):
    acces_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

