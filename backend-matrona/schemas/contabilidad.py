from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class VentaHistorialResponse(BaseModel):
    id_pedidos: int
    nombre_bebida: str
    cantidad: int
    fecha_pedido: date
    nombre_cliente: str
    total_venta: Decimal

    class Config:
        orm_mode = True

class IngresosPorProductoResponse(BaseModel):
    nombre_bebida: str
    total_ingresos: Decimal

    class Config:
        orm_mode = True