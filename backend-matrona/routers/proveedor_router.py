from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from db import get_db
from models import Proveedor, Materiales
from schemas.proveedor import ProveedorCreate, ProveedorOut, ProveedorMaterial, ProveedorBase, ProveedorModified

router = APIRouter(prefix="/proveedor", tags=["proveedores"])
#router para agregar proveedores
@router.post("/", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED)
def crear_proveedor(data: ProveedorCreate, db: Session = Depends(get_db)):
    nuevo_proveedor = Proveedor(**data.model_dump())# tengo que recordar que model dump me evitar escribir campo por campo y reasiganar cada valor
    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)
    return nuevo_proveedor

#router para actualizacion en cascada proveedor - materiales
# permite crear un proveedor completo con el material y cantidades que provee
@router.post("/material")
def proveedor_material_create(data: ProveedorMaterial, db: Session = Depends(get_db)):
   
        nuevo_proveedor = Proveedor(
            nombre_proveedor = data.nombre_proveedor,
            material_que_provee = data.material_que_provee,
            cantidadM = data.cantidadM,
            telefono = data.telefono,
            direccion_proveedor = data.direccion_proveedor,
            frecuencia_entrega = data.frecuencia_entrega,
        )
        db.add(nuevo_proveedor)
        db.flush()

        nuevo_material = Materiales(
            id_proveedor = nuevo_proveedor.id_proveedor,
            actividad = data.materiales.actividad,
            tipo_material = data.materiales.tipo_material,
            cantidad_disponible = data.materiales.cantidad_disponible,
            cantidad_a_agregar = data.materiales.cantidad_a_agregar,
        )
        db.add(nuevo_material)
        db.commit()
        db.refresh(nuevo_material)
        return nuevo_material
    

#router para obtener proveedores
@router.get("/", response_model=List[ProveedorBase])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(Proveedor).all()

#router para modificar el proveedor mediante su id
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