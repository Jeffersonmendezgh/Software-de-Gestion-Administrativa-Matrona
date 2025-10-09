from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Proveedor(Base):
    __tablename__= "proveedor"

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre_proveedor = Column(String(150), nullable=False)
    material_que_provee = Column(String(150), nullable=False)
    cantidadM = Column(String(20), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion_proveedor = Column(String(150), nullable=True)
    frecuencia_entrega = Column(String(45), nullable=True)

    #definicion de la relacion con materiales
    materiales = relationship("Materiales", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor(id={self.id_proveedor}, nombre='{self.nombre_proveedor}')>"