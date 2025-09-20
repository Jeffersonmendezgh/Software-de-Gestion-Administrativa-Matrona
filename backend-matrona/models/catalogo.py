from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Catalogo(Base):
    __tablename__ = "catalogo"

    id_catalogo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_inventario = Column(Integer, ForeignKey("inventario.id_inventario", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    descripcion = Column(String(300))
    alcohol = Column(String(20))
    contenido = Column(Integer, nullable=True)
    precio_unidad = Column(DECIMAL(10, 2), nullable=False)
    precio_sixpack = Column(DECIMAL(10, 2))
    precio_caja = Column(DECIMAL(10, 2))
    

    # relación con inventario
    inventario = relationship("Inventario", back_populates="catalogo")
    detalles = relationship("DetallePedido", back_populates="catalogo")#relacion con pedidos