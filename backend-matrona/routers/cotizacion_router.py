from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.cotizaciones import Cotizaciones
from models.catalogo import Catalogo
from schemas.cotizaciones import CotizacionCreate, CotizacionResponse
from db import get_db

router = APIRouter(prefix="/cotizacion", tags=["Cotizaciones"])


@router.post("/", response_model=CotizacionResponse)
def crear_cotizacion(data: CotizacionCreate, db: Session = Depends(get_db)):
    
    catalogo = db.query(Catalogo).filter(
        Catalogo.id_catalogo == data.id_catalogo
    ).first()

    if not catalogo:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    #  cálculo del precio
    if data.tipo == "unidad":
        precio = float(catalogo.precio_unidad)

    elif data.tipo == "sixpack":
        if catalogo.precio_sixpack:
            precio = float(catalogo.precio_sixpack)
        else:
            precio = float(catalogo.precio_unidad) * 6

    elif data.tipo == "caja":
        if catalogo.precio_caja:
            precio = float(catalogo.precio_caja)
        else:
            precio = float(catalogo.precio_unidad) * 24

    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    total = precio * data.cantidad

    nueva_cotizacion = Cotizaciones(
        id_catalogo=data.id_catalogo,
        cantidad_cotizado=data.cantidad,
        total_cotizacion=total
    )

    db.add(nueva_cotizacion)
    db.commit()
    db.refresh(nueva_cotizacion)

    return nueva_cotizacion

@router.get("/")
def listar_cotizaciones(db: Session = Depends(get_db)):
    data = db.query(Cotizaciones).all()
    return data
