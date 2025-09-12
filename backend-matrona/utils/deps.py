#dependencias para obtener usuario actual desde Token
# utils/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db import get_db
from models.usuario import Usuario
from schemas.usuario import TokenData
from config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(sub=user_id, role=payload.get("role"))
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id_usuarios == int(token_data.sub)).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    # si tu modelo tuviera `is_active`, lo checamos aquí
    return current_user

# Rol-based dependency (ejemplo: admin only)
def require_role(role_id: int):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.id_rol != role_id:
            raise HTTPException(status_code=403, detail="No tienes permisos")
        return current_user
    return role_checker
