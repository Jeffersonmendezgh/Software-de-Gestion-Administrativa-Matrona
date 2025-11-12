from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class UsuarioInfo(BaseModel):
    nombre: str
    apellido: str

    class Config:
        from_attributes = True


class ClienteInfo(BaseModel):
    id_cliente: int
    usuario: UsuarioInfo   #  accedemos a la relación con Usuario

    class Config:
        from_attributes = True


class DetallePedidoCreate(BaseModel):
    id_catalogo: int
    cantidad_pedido_uds: int
    presentacion: str

class DetallePedidoOut(BaseModel):
    id_detalle_pedido: int
    id_catalogo: Optional[int]
    cantidad_pedido_uds: Optional[int]
    precio_unitario: Optional[float]
    subtotal: Optional[float]
    presentacion: str
    nombre_bebida: Optional[str] = None

    
    catalogo_nombre: Optional[str] = None 

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    #id_cliente: int
    items: List[DetallePedidoCreate]

class PedidoOut(BaseModel):
    id_pedidos: int
    total_pedido: float
    fecha_pedido: date
    estado: str
    cliente: ClienteInfo
    detalles: List[DetallePedidoOut]

    class Config:
        from_attributes = True
