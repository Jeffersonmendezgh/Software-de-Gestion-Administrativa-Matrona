from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from typing import List
from models import Empleado, Usuario
from schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse
from sqlalchemy import func

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.get("/", response_model=List[EmpleadoResponse])
def listar_empleados(db: Session = Depends(get_db)):
    empleados = db.query(Empleado).join(Empleado.usuario).all()
    return empleados


#patch para editar empleado
@router.patch("/{id_empleado}", response_model=EmpleadoResponse)
def actualizar_empleado(id_empleado: int, empleado: EmpleadoUpdate, db: Session = Depends(get_db)):
    # Buscar empleado
    empleado_db = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado_db:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    #Actualizar datos del empleado
    for key, value in empleado.dict(exclude_unset=True).items():
        if key not in ["nombre", "apellido"]:  # estos dos van en Usuario
            setattr(empleado_db, key, value)

    #Actualizar nombre/apellido en usuario
    if empleado.nombre or empleado.apellido:
        usuario = empleado_db.usuario
        if empleado.nombre:
            usuario.nombre = empleado.nombre
        if empleado.apellido:
            usuario.apellido = empleado.apellido

    db.commit()
    db.refresh(empleado_db)
    return empleado_db