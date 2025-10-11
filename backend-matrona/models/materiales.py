from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Materiales(Base):
    __tablename__ = "materiales"

    id_materiales = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id_proveedor"), nullable=True)
    actividad = Column(String(20), nullable=False)
    tipo_material = Column(String(150), nullable=False)
    cantidad_disponible = Column(String(150), nullable=True)
    cantidad_a_agregar = Column(String(45), nullable=True)

    # Relación con proveedor (muchos a uno)
    proveedor = relationship("Proveedor", back_populates="materiales")

    def __repr__(self):
        return f"<Materiales(id={self.id_materiales}, tipo='{self.tipo_material}')>"
