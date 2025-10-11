from  sqlalchemy import Integer, DECIMAL, ForeignKey, Column
from sqlalchemy.orm import relationship
from db import Base

class Contabilidad(Base):
    __tablename__ = "contabilidad"
    id_contabilidad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_administrador = Column(Integer, ForeignKey("administrador.id_administrador"), nullable=False)
    total_presupuesto = Column(DECIMAL, nullable=False)
    ingresos = Column(DECIMAL,nullable=True)

    admin = relationship("Administrador", back_populates="contabilidad")
