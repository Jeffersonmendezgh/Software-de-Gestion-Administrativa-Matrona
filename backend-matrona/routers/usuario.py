# routers/usuario.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Usuario, Rol
from schemas import UsuarioBase, UsuarioCreate, UsuarioPut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioBase])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/", response_model=UsuarioBase)# response indica que la respuesta debe ser igual q la estructura del modelo base q tenemos en schemas
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):#recibe parametro usuario que debe seguir la estructura del modelo usuariocreate
    rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol).first()#busca en la table rol un id_rol que coinciada con el que viene de id usuario
    if not rol:
        raise HTTPException(status_code=400, detail="Rol no válido")

    db_usuario = Usuario(**usuario.dict())# convierte los datos a formato dict los toma y los pasa como parametros
    db.add(db_usuario)#se prepara para save new user
    db.commit()#guarda en la db
    db.refresh(db_usuario) #actualiza
    return db_usuario #retorna datos creados

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

@router.delete("/{id_usuarios}")
def eliminar_usuario(id_usuarios: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuarios == id_usuarios).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_usuario)
    db.commit()
    return {"mensaje": f"Usuario con id {id_usuarios} eliminado"}
