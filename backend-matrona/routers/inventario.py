# routers/inventario.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from db import get_db
from models import Inventario
from schemas.inventario import InventarioBase, InventarioCreate, InventarioUpdate, StockUpdate

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/", response_model=List[InventarioBase])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@router.get("/{id_inventario}", response_model=InventarioBase)
def obtener_item(id_inventario: int, db: Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id_inventario == id_inventario).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@router.post("/", response_model=InventarioBase, status_code=status.HTTP_201_CREATED)
def crear_item(payload: InventarioCreate, db: Session = Depends(get_db)):
    # chequear nombre único
    existente = db.query(Inventario).filter(Inventario.nombre_bebida == payload.nombre_bebida).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un item con ese nombre_bebida")

    nuevo = Inventario(
        nombre_bebida=payload.nombre_bebida,
        cantidad_disponible=payload.cantidad_disponible or 0,
        ultimo_movimiento=payload.ultimo_movimiento,
        unidades_agregadas=payload.unidades_agregadas
    )
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el item")
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_inventario}", response_model=InventarioBase)
def reemplazar_item(id_inventario: int, payload: InventarioCreate, db: Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id_inventario == id_inventario).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    # si se cambia el nombre, comprobar que no exista otro con ese nombre
    if payload.nombre_bebida != item.nombre_bebida:
        otro = db.query(Inventario).filter(Inventario.nombre_bebida == payload.nombre_bebida).first()
        if otro:
            raise HTTPException(status_code=400, detail="Otro item ya tiene ese nombre_bebida")

    item.nombre_bebida = payload.nombre_bebida
    item.cantidad_disponible = payload.cantidad_disponible or 0
    item.ultimo_movimiento = payload.ultimo_movimiento
    item.unidades_agregadas = payload.unidades_agregadas

    db.commit()
    db.refresh(item)
    return item

@router.patch("/{id_inventario}", response_model=InventarioBase)
def actualizar_parcial(id_inventario: int, payload: InventarioUpdate, db: Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id_inventario == id_inventario).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    datos = payload.dict(exclude_unset=True)
    if "nombre_bebida" in datos:
        # verificar unicidad si cambia nombre
        if datos["nombre_bebida"] != item.nombre_bebida:
            otro = db.query(Inventario).filter(Inventario.nombre_bebida == datos["nombre_bebida"]).first()
            if otro:
                raise HTTPException(status_code=400, detail="Otro item ya tiene ese nombre_bebida")

    for campo, valor in datos.items():
        setattr(item, campo, valor)

    db.commit()
    db.refresh(item)
    return item

#parch para agregar cervezas
@router.patch("/agregar-stock/{id_inventario}", response_model=InventarioBase)
def agregar_stock(id_inventario: int, payload: StockUpdate, db:Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id_inventario == id_inventario).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    #sumar unidades con un metodo de una clase
    try:
        item.agregar_stock(payload.unidades)  # ✅ Usamos el método del modelo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    db.commit()
    db.refresh(item)
    return item
    

@router.delete("/{id_inventario}")
def eliminar_item(id_inventario: int, db: Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id_inventario == id_inventario).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(item)
    db.commit()
    return {"mensaje": f"Item {id_inventario} eliminado"}
