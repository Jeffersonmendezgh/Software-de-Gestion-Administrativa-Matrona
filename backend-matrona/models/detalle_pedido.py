from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from db import Base

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_pedidos = Column(Integer, ForeignKey("pedidos.id_pedidos"), nullable=False)
    id_catalogo = Column(Integer, ForeignKey("catalogo.id_catalogo"), nullable=True)#especial atencion a nullo y no null
    precio_unitario = Column(Numeric(10,2), nullable=True)
    subtotal = Column(Numeric(10,2), nullable=True)
    cantidad_pedido_uds = Column(Integer, nullable=True)
    presentacion = Column(String(20), nullable=False)
    #relaciones con pedido y catalogo
    pedido = relationship("Pedido", back_populates="detalles")
    catalogo = relationship("Catalogo", back_populates="detalles")
    #  propiedad que expone el string
    @property
    def catalogo_nombre(self):
        return self.catalogo.descripcion if self.catalogo else None
    
