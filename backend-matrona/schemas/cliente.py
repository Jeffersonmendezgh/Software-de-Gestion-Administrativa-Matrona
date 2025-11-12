from pydantic import BaseModel
from datetime import date
from typing import Optional
from schemas.usuario import UsuarioBase

# Este lo usamos para crear un cliente
class ClienteCreate(BaseModel):
    id_usuarios: int   # FK al usuario 
    fecha_registro: date

# Este lo usamos para leer/retornar un cliente
class ClienteOut(BaseModel):
    id_cliente: int
    fecha_registro: date
    usuario: UsuarioBase

    class Config:
        orm_mode = True

