# routers/usuario.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Usuario, Rol
from schemas import UsuarioBase, UsuarioCreate, UsuarioPut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

#obtener usuarios
@router.get("/", response_model=list[UsuarioBase])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

#crear usuario
@router.post("/", response_model=UsuarioBase)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol).first()
    if not rol:
        raise HTTPException(status_code=400, detail="Rol no válido")

    db_usuario = Usuario(**usuario.model_dump())
    db.add(db_usuario)#se prepara para save new user
    db.commit()
    db.refresh(db_usuario) 
    return db_usuario #retorna datos creados

#editar usuario
@router.put("/{id_usuarios}", response_model=UsuarioPut)
def reemplazar_usuario(id_usuarios: int, usuario: UsuarioPut, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuarios == id_usuarios).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol).first()
    if not rol:
        raise HTTPException(status_code=400, detail="Rol no válido")

    existe = db.query(Usuario).filter(Usuario.correo == usuario.correo, Usuario.id_usuarios != id_usuarios).first()
    if existe:
        raise HTTPException(status_code=400, detail="Correo ya está en uso")

    db_usuario.id_rol = usuario.id_rol
    db_usuario.nombre = usuario.nombre
    db_usuario.apellido = usuario.apellido
    db_usuario.correo = usuario.correo
    db_usuario.contrasena = usuario.contrasena
    db_usuario.direccion = usuario.direccion

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

#eliminar usuario
@router.delete("/{id_usuarios}")
def eliminar_usuario(id_usuarios: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuarios == id_usuarios).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_usuario)
    db.commit()
    return {"mensaje": f"Usuario con id {id_usuarios} eliminado"}
