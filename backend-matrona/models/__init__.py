# models/__init__.py
from .usuario import Usuario
from .rol import Rol
from .inventario import Inventario
from .catalogo import Catalogo
from .cliente import Cliente
from .pedidos import Pedido
from .detalle_pedido import DetallePedido
from .proveedor import Proveedor
from .materiales import Materiales


__all__ = ["Usuario", "Rol", "Inventario", "Catalogo", "Cliente", "Pedido", "DetallePedido", "Proveedor", "Materiales"]