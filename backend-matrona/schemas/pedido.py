from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# =========================
# Usuario (para mostrar datos de cliente)
# =========================
class UsuarioInfo(BaseModel):
    nombre: str
    apellido: str

    class Config:
        orm_mode = True

# =========================
# Cliente
# =========================
class ClienteInfo(BaseModel):
    id_cliente: int
    usuario: UsuarioInfo   # 👈 accedemos a la relación con Usuario

    class Config:
        orm_mode = True

# =========================
# Detalle del pedido
# =========================
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

    # Aquí usamos descripcion en lugar de nombre
    catalogo_nombre: Optional[str] = None 

    class Config:
        orm_mode = True

# =========================
# Pedido
# =========================
class PedidoCreate(BaseModel):
    id_cliente: int
    items: List[DetallePedidoCreate]

class PedidoOut(BaseModel):
    id_pedidos: int
    total_pedido: float
    fecha_pedido: date
    estado: str
    cliente: ClienteInfo
    detalles: List[DetallePedidoOut]

    class Config:
        orm_mode = True
