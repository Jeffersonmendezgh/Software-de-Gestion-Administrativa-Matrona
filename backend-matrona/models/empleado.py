from sqlalchemy import Column, Integer, Date, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from db import Base

class Empleado(Base):
    __tablename__ = "empleado"
    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey("usuarios.id_usuarios"), nullable=False)
    fecha_contratacion = Column(Date, nullable=False)
    salario = (Column(DECIMAL, nullable=False))
    fecha_pago = (Column(Date, nullable=False))
    area_laboral = Column(String, nullable=True)
    telefono_empleado = Column(String, nullable=True)
    
    usuario = relationship("Usuario", back_populates="empleado")


