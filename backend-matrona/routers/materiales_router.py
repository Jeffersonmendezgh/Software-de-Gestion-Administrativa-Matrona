from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models.materiales import Materiales
from schemas.materiales import MaterialCreate, MaterialUpdate, MaterialResponse
from typing import List

router = APIRouter(prefix="/api/materiales", tags=["Materiales"])

# ✅ Obtener todos los materiales
@router.get("/", response_model=List[MaterialResponse])
def obtener_materiales(db: Session = Depends(get_db)):
    materiales = db.query(Materiales).all()
    return materiales


@router.post("/", response_model=MaterialResponse)
def crear_material(material: MaterialCreate, db: Session = Depends(get_db)):
    nuevo_material = Materiales(
        tipo_material=material.tipo_material,
        cantidad_a_agregar=material.cantidad_a_agregar,
        actividad = material.actividad,
        cantidad_disponible=None,  # dejemos opcional por ahora
        id_proveedor=None          # aca igual
    )

    db.add(nuevo_material)
    db.commit()
    db.refresh(nuevo_material)
    return nuevo_material

#put para editar mediante el modal
@router.put("/{id_material}", response_model=MaterialResponse)
def actualizar_material(id_material: int, material: MaterialCreate, db: Session = Depends(get_db)):
    material_db = db.query(Materiales).filter(Materiales.id_materiales == id_material).first()
    if not material_db:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    
    material_db.tipo_material = material.tipo_material
    material_db.cantidad_a_agregar = material.cantidad_a_agregar

    db.commit()
    db.refresh(material_db)
    return material_db

#  Eliminar un material
@router.delete("/{id_material}")
def eliminar_material(id_material: int, db: Session = Depends(get_db)):
    material_db = db.query(Materiales).filter(Materiales.id_materiales == id_material).first()
    if not material_db:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    db.delete(material_db)
    db.commit()
    return {"mensaje": "Material eliminado correctamente"}
