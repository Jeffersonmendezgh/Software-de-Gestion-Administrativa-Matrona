# schemas/inventario.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InventarioBase(BaseModel):
    id_inventario: int
    nombre_bebida: str
    cantidad_disponible: int
    ultimo_movimiento: Optional[datetime] = None
    unidades_agregadas: Optional[int] = None

    class Config:
        orm_mode = True

class InventarioCreate(BaseModel):
    nombre_bebida: str
    cantidad_disponible: Optional[int] = 0
    ultimo_movimiento: Optional[datetime] = None
    unidades_agregadas: Optional[int] = None

class InventarioUpdate(BaseModel):
    nombre_bebida: Optional[str] = None
    cantidad_disponible: Optional[int] = None
    ultimo_movimiento: Optional[datetime] = None
    unidades_agregadas: Optional[int] = None


class StockUpdate(BaseModel):
    unidades: int