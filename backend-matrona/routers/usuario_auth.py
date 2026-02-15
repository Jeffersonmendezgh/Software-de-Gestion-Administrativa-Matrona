# routers/usuario_auth.py
from fastapi import APIRouter, Depends, HTTPException, Response, Form
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
from datetime import timedelta
from fastapi.responses import RedirectResponse



router = APIRouter(prefix="/auth", tags=["Usuarios"])

# Registro de usuarios en la db
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

# Login, aca  se crea el token de acceso y se envia en la coockie  
# se da autorizacion al usuario y se redirije segun rol que provee JWT token
@router.post("/login")
def login(
    # parametros configurados para iniciar sesion desde el form
    correo: str = Form(...), 
    contrasena: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not user or not verify_password(contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {"sub": str(user.id_usuarios), "role": str(user.id_rol)}
    access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))

    # Decide la URL según el rol
    if user.id_rol == 1:
        redirect_url = "/menu"
    elif user.id_rol == 2:
        redirect_url = "/empleados/interfaz"
    elif user.id_rol == 3:
        redirect_url = "/catalogo"
    else:
        redirect_url = "/"

    # Crea el objeto de redirección y configura la cookie en él
    redirect = RedirectResponse(url=redirect_url, status_code=303)
    redirect.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True, #no accesible desde js
        samesite="lax",
        secure=False,  # True en producción con HTTPS no puedo olvidarlo
        max_age=30 * 60 #tiempo de vida de la coockie en secs
    )
    return redirect


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

#router para cerrar la sesion
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message":"Sesion cerrada correctamente"}