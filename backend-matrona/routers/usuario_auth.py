#registro y login
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models.usuario import Usuario
from models.rol import Rol
from schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioLogin, Token
from utils.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from utils.deps import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Usuarios"])
#registro post usuarios/registro
@router.post("/registro", response_model=UsuarioOut)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    #validamos correo unico
    existe = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="correo ya esta registrado")
    #validamos ahora rol
    if usuario.id_rol:
        rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol).first()
        if not rol:
            raise HTTPException(status_code=400, detail="Rol invalido")
        
        hashed = get_password_hash(usuario.contrasena)
        db_usuario = Usuario(
            id_rol = usuario.id_rol,
            nombre = usuario.nombre,
            apellido = usuario.apellido,
            correo = usuario.correo,
            contrasena = hashed,
            direccion = usuario.direccion
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

#login post usuarios/login que devuelve el JWT
@router.post("/login", response_model=Token)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    if not verify_password(data.contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales invaliadas")
    
    token_data = {"sub": str(user.id_usuarios), "role": str(user.id_rol)}
    access_token = create_access_token(token_data)
    return{"access_token": access_token, "token_type": "bearer"}

#proteccion para las rutas mediante el rol

@router.get("/protegido")
def ruta_protegida(current_user = Depends(get_current_user)):
    return {"msg": f"Hola {current_user.nombre}, estas autenticado"}

@router.delete("/{id}", dependencies=[Depends(require_role(1))])  # 1 = administrador
def borrar_usuario(id: int):
    # solo admin puede
    ...