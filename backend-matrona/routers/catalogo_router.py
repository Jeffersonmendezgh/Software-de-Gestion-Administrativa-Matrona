from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db import get_db
from models.catalogo import Catalogo
from models.inventario import Inventario
from schemas.catalogo import CatalogoBase, CatalogoCreate
from typing import List
from datetime import datetime, timezone

router = APIRouter(prefix="/catalogo", tags=["Catálogo"])

# 📌 Crear un registro de catálogo
@router.post("/", response_model=CatalogoBase)
def crear_catalogo(data: CatalogoCreate, db: Session = Depends(get_db)):
    try:
    # Paso 1: Crear inventario (sin contenido, va en catálogo)
        nuevo_inventario = Inventario(
            nombre_bebida=data.nombre_bebida,
            cantidad_disponible=data.cantidad_disponible,
            unidades_agregadas=data.cantidad_disponible,  # primera vez = stock inicial
            ultimo_movimiento=datetime.now(timezone.utc)
        )
        db.add(nuevo_inventario)
        db.flush()    # ejecuta INSERT en BD pero NO confirma la transacción: ahora existe id     

        # Paso 2: Crear catálogo asociado (aquí sí va contenido)
        nuevo_catalogo = Catalogo(
            id_inventario=nuevo_inventario.id_inventario,
            descripcion=data.descripcion,
            contenido=data.contenido,   
            alcohol=data.alcohol,
            precio_unidad=data.precio_unidad,
            precio_sixpack=data.precio_sixpack,
            precio_caja=data.precio_caja
        )
        db.add(nuevo_catalogo) 
        db.commit()
        db.refresh(nuevo_catalogo)

        return nuevo_catalogo

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear producto")


# 📌 Obtener todo el catálogo
@router.get("/", response_model=List[CatalogoBase])
def listar_catalogo(db: Session = Depends(get_db)):
    return db.query(Catalogo).all()

# 📌 Obtener un registro por id
@router.get("/{id_catalogo}", response_model=CatalogoBase)
def obtener_catalogo(id_catalogo: int, db: Session = Depends(get_db)):
    catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == id_catalogo).first()
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return catalogo

# 📌 PUT para actualizar catálogo + inventario
@router.put("/{id_catalogo}", response_model=CatalogoBase)
def actualizar_catalogo(id_catalogo: int, data: CatalogoCreate, db: Session = Depends(get_db)):
    # 1️⃣ Buscar el registro de catálogo
    catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == id_catalogo).first()
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")

    # 2️⃣ Buscar inventario asociado
    inventario = db.query(Inventario).filter(Inventario.id_inventario == catalogo.id_inventario).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    # 3️⃣ Actualizar inventario
    inventario.nombre_bebida = data.nombre_bebida
    inventario.cantidad_disponible += data.cantidad_disponible  # sumamos al stock
    inventario.unidades_agregadas = data.cantidad_disponible    # las nuevas agregadas
    inventario.ultimo_movimiento = datetime.now()               # fecha actual
    inventario.contenido = data.contenido                       # nuevo contenido

    # 4️⃣ Actualizar catálogo
    catalogo.descripcion = data.descripcion
    catalogo.alcohol = data.alcohol
    catalogo.precio_unidad = data.precio_unidad
    catalogo.precio_sixpack = data.precio_sixpack
    catalogo.precio_caja = data.precio_caja

    db.commit()
    db.refresh(catalogo)

    return catalogo

# 📌 Eliminar un registro de catálogo
@router.delete("/{id_catalogo}")
def eliminar_catalogo(id_catalogo: int, db: Session = Depends(get_db)):
    catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == id_catalogo).first()
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")

    # Al eliminar el catálogo, también eliminamos el inventario asociado
    inventario = db.query(Inventario).filter(Inventario.id_inventario == catalogo.id_inventario).first()
    if inventario:
        db.delete(inventario)

    db.delete(catalogo)
    db.commit()
    return {"ok": True, "mensaje": f"Catálogo {id_catalogo} eliminado correctamente"}
