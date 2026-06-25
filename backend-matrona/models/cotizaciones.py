from sqlalchemy import Column, Integer, DECIMAL, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Cotizaciones(Base):
    __tablename__ = "cotizaciones"
    id_cotizacion = Column(Integer, primary_key=True, nullable=False, index=True)
    id_catalogo = Column(Integer, ForeignKey("catalogo.id_catalogo"), nullable=False)
    cantidad_cotizado = Column(Integer, nullable=False)
    total_cotizacion = Column(DECIMAL(10,2), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)

    catalogo = relationship("Catalogo", back_populates="cotizaciones")
