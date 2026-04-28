from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal

class VentaHistorialResponse(BaseModel):
    id_pedidos: int
    nombre_bebida: str
    cantidad: int
    fecha_pedido: date
    nombre_cliente: str
    total_venta: Decimal

    model_config = ConfigDict(from_attributes=True)

class IngresosPorProductoResponse(BaseModel):
    nombre_bebida: str
    total_ingresos: Decimal

    model_config = ConfigDict(from_attributes=True)