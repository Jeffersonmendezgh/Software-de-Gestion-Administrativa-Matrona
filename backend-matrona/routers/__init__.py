from .usuario import router as usuario_router
from .inventario import router as inventario_router
from .ws_router import router as ws_router

__all__ = ["usuario_router", "inventario_router", "ws_router"]