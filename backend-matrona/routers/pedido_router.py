from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from db import get_db
from decimal import Decimal
from datetime import date
from models.pedidos import Pedido
from models.detalle_pedido import DetallePedido
from models.catalogo import Catalogo
from models.inventario import Inventario
from schemas.pedido import PedidoCreate, PedidoOut
from utils.websoket import manager
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
#postpara crear el pedido nuevo al hacer click en catalogo
@router.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def crear_pedido(data: PedidoCreate, db: Session = Depends(get_db), bg: BackgroundTasks = None):
    try:
        with db.begin():  # transacción
            # crear pedido base
            pedido = Pedido(
                id_cliente=data.id_cliente,
                fecha_pedido=date.today(),
                total_pedido=Decimal("0.00")
            )
            db.add(pedido)
            db.flush()  # obtener id_pedidos

            total = Decimal("0.00")
            # procesar items
            for it in data.items:
                catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == it.id_catalogo).first()
                if not catalogo:
                    raise HTTPException(status_code=404, detail=f"Catalogo {it.id_catalogo} no existe")

                # obtener inventario y bloquear la fila para evitar sobreventa (simple)
                inventario = db.query(Inventario).filter(Inventario.id_inventario == catalogo.id_inventario).with_for_update().first()
                if not inventario:
                    raise HTTPException(status_code=404, detail="Inventario no encontrado")
                if inventario.cantidad_disponible < it.cantidad_pedido_uds:
                    raise HTTPException(status_code=400, detail=f"Stock insuficiente para {catalogo.id_catalogo}")

                precio = catalogo.precio_unidad or Decimal("0.00")
                subtotal = Decimal(precio) * int(it.cantidad_pedido_uds)

                # decrementar stock
                #inventario.cantidad_disponible -= it.cantidad_pedido_uds
                #db.add(inventario)

                detalle = DetallePedido(
                    id_pedidos=pedido.id_pedidos,
                    id_catalogo=catalogo.id_catalogo,
                    precio_unitario=precio,
                    subtotal=subtotal,
                    cantidad_pedido_uds=it.cantidad_pedido_uds,
                    presentacion=it.presentacion
                )
                db.add(detalle)
                total += subtotal

            # actualizar total
            pedido.total_pedido = total
            db.add(pedido)
            # commit por with db.begin()

        # notificar a admins vía websocket (programar tarea no-bloqueante)
        if bg is not None:
            bg.add_task(manager.broadcast_json_sync, {
                "type": "new_order",
                "id_pedidos": pedido.id_pedidos,
                "summary": f"Pedido {pedido.id_pedidos} - {len(data.items)} items - total {float(total)}"
            })

        db.refresh(pedido)
        return pedido

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")
    
#  Endpoint para entregar pedido es decir cambiar el estado de pediente a entregado
@router.put("/{pedido_id}/estado")
def entregar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    # 1. Buscar pedido
    pedido = db.query(Pedido).filter(Pedido.id_pedidos == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # 2. Verificar si ya está entregado
    if pedido.estado == "entregado":
        raise HTTPException(status_code=400, detail="El pedido ya fue entregado")

    # 3. Cambiar estado a entregado
    pedido.estado = "entregado"

    # 4. Restar inventario en cada detalle del pedido
    detalles = db.query(DetallePedido).filter(DetallePedido.id_pedidos == pedido_id).all()
    for detalle in detalles:
        catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == detalle.id_catalogo).first()
        if not catalogo:
            raise HTTPException(status_code=404, detail=f"Catálogo {detalle.id_catalogo} no encontrado")

        inventario = db.query(Inventario).filter(Inventario.id_inventario == catalogo.id_inventario).first()
        if not inventario:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        if inventario.cantidad_disponible < detalle.cantidad_pedido_uds:
            raise HTTPException(status_code=400, detail="Inventario insuficiente para entregar pedido")

        inventario.cantidad_disponible -= detalle.cantidad_pedido_uds
        db.add(inventario)

    db.commit()
    db.refresh(pedido)

    return {"message": f"Pedido {pedido_id} entregado con éxito", "estado": pedido.estado}

# get para llevar los pedios al fronted
@router.get("/", response_model=list[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    return pedidos