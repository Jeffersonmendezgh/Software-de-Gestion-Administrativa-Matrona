from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey("usuarios.id_usuarios"), nullable=False, unique=True)
    fecha_registro = Column(Date, nullable=False)

    # 👇 Relación con Usuario
    usuario = relationship("Usuario", back_populates="cliente", uselist=False)

    # 👇 Relación con Pedido (uno a muchos)
    pedidos = relationship("Pedido", back_populates="cliente")
