# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base
#rol
class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, autoincrement=False)  # IDs fijos (1=Admin, 2=Empleado, 3=Cliente)
    nombre_rol = Column(String(100), nullable=False)