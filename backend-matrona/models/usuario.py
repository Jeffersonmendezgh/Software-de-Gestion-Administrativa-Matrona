#Usuarios
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Usuario(Base):
    __tablename__ = "usuarios"   

    id_usuarios = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=True)
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    correo = Column(String(150), nullable=False)
    contrasena = Column("contraseña", String(255), nullable=False)  
    direccion = Column(String(200), nullable=True)
    rol = relationship("Rol")

    #relacion con cliente
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)

