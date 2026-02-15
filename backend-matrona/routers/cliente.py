from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.cliente import Cliente
from models.usuario import Usuario
from schemas.cliente import ClienteCreate, ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])
"""
@router.post("/", response_model=ClienteOut)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    # Validamos que exista el usuario
    usuario = db.query(Usuario).filter(Usuario.id_usuarios == cliente.id_usuarios).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    #  Creamos el cliente
    nuevo_cliente = Cliente(
        id_usuarios=cliente.id_usuarios,
        fecha_registro=cliente.fecha_registro
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente
"""
#router para obtener el listado de clientes en la db
@router.get("/", response_model=list[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return  db.query(Cliente).all()
    
