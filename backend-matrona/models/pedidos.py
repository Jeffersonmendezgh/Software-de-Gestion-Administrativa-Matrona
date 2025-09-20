from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, Enum
from sqlalchemy.orm import relationship
from db import Base
from datetime import date

class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedidos = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    total_pedido = Column(Numeric(10,2), nullable=False, default=0)
    fecha_pedido = Column(Date, nullable=False, default=date.today)
    estado = Column(Enum("pendiente", "entregado"), default="pendiente", nullable=False)
    #relaciones con cliente/detalle-pedidos. atencion especial a la columna con numeric, hay que verificar como funciona
    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")