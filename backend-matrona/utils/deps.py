#dependencias para obtener usuario actual desde Token
# utils/deps.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db import get_db
from models.usuario import Usuario
from schemas.usuario import TokenData
from config import SECRET_KEY, ALGORITHM

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(Usuario).filter(Usuario.id_usuarios == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user


def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    return current_user

# verificar aca q tenga rol valido
def require_role(role_id: int):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.id_rol != role_id:
            raise HTTPException(status_code=403, detail="No tienes permisos")
        return current_user
    return role_checker
