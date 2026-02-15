from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import Proveedor
from schemas.proveedor import ProveedorCreate, ProveedorOut, ProveedorBase, ProveedorModified

router = APIRouter(prefix="/proveedor", tags=["proveedores"])
#router para agrgar proveedores
@router.post("/", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED)
def crear_proveedor(data: ProveedorCreate, db: Session = Depends(get_db)):
    nuevo_proveedor = Proveedor(**data.model_dump())# tengo que recordar que model dump me evitar escribir campo por campo y reasiganar cada valor
    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)
    return nuevo_proveedor

#router para obtener proveedores
@router.get("/", response_model=List[ProveedorBase])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(Proveedor).all()

#router para modificar el proveedor
@router.patch("/edit/{id_proveedor}")
def modificar_proveedor(id_proveedor: str, data: ProveedorModified, db:Session = Depends(get_db)):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=400, detail="no se encontro proveedor")
    data_dict = data.dict(exclude_unset=True)
    for campo, valor in data_dict.items():
        setattr(proveedor, campo, valor)
    db.commit()
    db.refresh(proveedor)
    return proveedor