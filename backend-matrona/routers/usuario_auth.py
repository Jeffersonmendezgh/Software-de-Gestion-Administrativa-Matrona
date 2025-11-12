# routers/usuario_auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from datetime import date
from models.usuario import Usuario
from models.rol import Rol
from models.cliente import Cliente
from models.empleado import Empleado
from schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioLogin, Token
from utils.auth import get_password_hash, verify_password, create_access_token
from utils.deps import get_current_user, require_role


router = APIRouter(prefix="/auth", tags=["Usuarios"])

# Registro
@router.post("/registro", response_model=UsuarioOut)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Validar correo único
    existe = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Correo ya está registrado")

    # Validar rol
    if usuario.id_rol:
        rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol).first()
        if not rol:
            raise HTTPException(status_code=400, detail="Rol inválido")

    # Hashear contraseña
    hashed = get_password_hash(usuario.contrasena)

    db_usuario = Usuario(
        id_rol=usuario.id_rol,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        contrasena=hashed,
        direccion=usuario.direccion
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

#creamos la vinculacion con la tabla cliente
   # if else para que me quede mas claro
    if db_usuario.id_rol == 3:
        nuevo_cliente = Cliente(
            id_usuarios=db_usuario.id_usuarios,
            fecha_registro=date.today()
        )
        db.add(nuevo_cliente)

    elif db_usuario.id_rol == 2:
        nuevo_empleado = Empleado(
            id_usuarios=db_usuario.id_usuarios,
            fecha_contratacion=date.today(),  # Obligatorio tengo que poner por defecto
            salario=0,                     # sino pongo nada se me romple el modelo archemy
            fecha_pago=date.today(),          # luego con PATCH lo arreglo directamente con lo que venga del front
            area_laboral=None,
            telefono_empleado=None
        )
        db.add(nuevo_empleado)

    db.commit()  # Guarda cliente o empleado
    return db_usuario
# Login
@router.post("/login", response_model=Token)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not verify_password(data.contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {"sub": str(user.id_usuarios), "role": str(user.id_rol)}
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida
@router.get("/protegido")
def ruta_protegida(current_user=Depends(get_current_user)):
    return {"msg": f"Hola {current_user.nombre}, estás autenticado"}


#endpoint para eliminar
@router.delete("/{id}", dependencies=[Depends(require_role(1))])  # 1 = administrador
def borrar_usuario(id: int):

    return {"msg": f"Usuario con id {id} eliminado "}

#router para obtener en el fronted mediante el token el usuario logeado
@router.get("/me")
def get_me(current_user: Usuario = Depends(get_current_user)):
    return {
        "id_usuarios": current_user.id_usuarios,
        "nombre": current_user.nombre,
        "apellido": current_user.apellido,
        "rol": current_user.id_rol
    }