# modelsinventario.py
from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Inventario(Base):
    __tablename__ = "inventario"

    id_inventario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_bebida = Column(String(100), nullable=False, unique=True)
    cantidad_disponible = Column(Integer, nullable=False, default=0)
    ultimo_movimiento = Column(DateTime, nullable=True)
    unidades_agregadas = Column(Integer, nullable=True)
    catalogo = relationship("Catalogo", back_populates="inventario", uselist=False, cascade="all, delete")

     #  Método para manejar stock
    def agregar_stock(self, unidades: int):
        if unidades <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor a 0")
        self.cantidad_disponible += unidades
        self.unidades_agregadas = unidades
        self.ultimo_movimiento = datetime.now()