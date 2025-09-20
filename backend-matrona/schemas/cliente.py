from pydantic import BaseModel
from datetime import date

# Este lo usamos para crear un cliente
class ClienteCreate(BaseModel):
    id_usuarios: int   # FK al usuario ya existente
    fecha_registro: date

# Este lo usamos para leer/retornar un cliente
class ClienteOut(BaseModel):
    id_cliente: int
    id_usuarios: int
    fecha_registro: date

    class Config:
        orm_mode = True
