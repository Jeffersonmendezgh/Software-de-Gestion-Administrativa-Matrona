from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal


class CatalogoInfo(BaseModel):
    id_catalogo: int
    descripcion: Optional[str]
    alcohol: Optional[str]
    contenido: Optional[int]
    precio_unidad: Decimal
    precio_sixpack: Optional[Decimal]
    precio_caja: Optional[Decimal]
    

    class Config:
        orm_mode = True


class CotizacionResponse(BaseModel):
    id_cotizacion: int
    cantidad_cotizado: int
    total_cotizacion: float
    fecha_hora: datetime

    catalogo: CatalogoInfo

    class Config:
        orm_mode = True

class CotizacionCreate(BaseModel):
    id_catalogo: int
    cantidad: int
    tipo: Literal["unidad", "sixpack", "caja"]