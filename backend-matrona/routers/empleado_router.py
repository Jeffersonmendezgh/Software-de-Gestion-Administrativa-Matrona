from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from typing import List
from models import Empleado, Usuario
from schemas.empleado import EmpleadoCreate, EmpleadoMeActual, EmpleadoUpdate, EmpleadoResponse, EmpleadoMeResponse
from sqlalchemy import func
from utils.deps import get_current_user

router = APIRouter(prefix="/empleados", tags=["Empleados"])

#router para listar a todos los empleados
@router.get("/", response_model=List[EmpleadoResponse])
def listar_empleados(db: Session = Depends(get_db)):
    empleados = db.query(Empleado).join(Empleado.usuario).all()
    return empleados

#router para acceder al empleado en session
@router.get("/actual", response_model=EmpleadoMeActual)
def empleado_actual(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id_usuarios == current_user.id_usuarios).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return {
        "usuario": {
            "nombre": current_user.nombre,
            "apellido": current_user.apellido
        },
        "area_laboral": empleado.area_laboral,
        "salario": empleado.salario,  
        "fecha_contratacion": empleado.fecha_contratacion,
        "fecha_pago": empleado.fecha_pago
    }

#patch para modificar el empleado mediante el respectivo id
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



#endpoint para eliminar empleados
@router.delete("/{id_empleado}")
def eliminar_empleado(id_empleado: int, db: Session = Depends(get_db)):
    db_empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not db_empleado:
        raise HTTPException(status_code=404, detail="empleado no encontrado")
    db.delete(db_empleado)
    db.commit()
    return {f"Empleado con id {id_empleado} eliminado"}

# router para obtener al empleado vinculado al id usuario mediante join
@router.get("/{id_usuario}", response_model=EmpleadoMeResponse)
def obtener_empleado_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    # Buscar al empleado y su relación con usuario
    empleado = (
        db.query(Empleado)
        .join(Usuario)
        .filter(Empleado.id_usuarios == id_usuario)
        .first()
    )

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return {
        "usuario": {
            "id_usuarios": empleado.usuario.id_usuarios,
            "nombre": empleado.usuario.nombre,
            "apellido": empleado.usuario.apellido,
            "rol": empleado.usuario.id_rol
        },
        "area_laboral": empleado.area_laboral,
        "salario": empleado.salario,
        "fecha_contratacion": empleado.fecha_contratacion,
        "fecha_pago": empleado.fecha_pago
    }

