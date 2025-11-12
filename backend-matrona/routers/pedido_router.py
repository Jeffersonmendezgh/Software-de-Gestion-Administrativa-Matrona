from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from db import get_db
from decimal import Decimal
from datetime import date
from utils.deps import get_current_user
from models.usuario import Usuario
from models.cliente import Cliente
from models.pedidos import Pedido
from models.detalle_pedido import DetallePedido
from models.catalogo import Catalogo
from models.inventario import Inventario
from schemas.pedido import PedidoCreate, PedidoOut
from utils.websocket import manager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
#from routers.ws_router import broadcast

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
#postpara crear el pedido nuevo al hacer click en catalogo
@router.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate,
    db: Session = Depends(get_db),
    bg: BackgroundTasks = None,
    current_user: Usuario = Depends(get_current_user)
):
    try:
        # buscar cliente vinculado al usuario logeado
        cliente = db.query(Cliente).filter(Cliente.id_usuarios == current_user.id_usuarios).first()
        if not cliente:
            raise HTTPException(status_code=400, detail="El usuario no está registrado como cliente")

        # crear pedido base
        pedido = Pedido(
            id_cliente=cliente.id_cliente,
            fecha_pedido=date.today(),
            total_pedido=Decimal("0.00")
        )
        db.add(pedido)
        db.flush()  # para obtener id_pedidos

        total = Decimal("0.00")

        # procesar items
        for it in data.items:
            catalogo = db.query(Catalogo).filter(
                Catalogo.id_catalogo == it.id_catalogo
            ).first()
            if not catalogo:
                raise HTTPException(status_code=404, detail=f"Catalogo {it.id_catalogo} no existe")

            inventario = db.query(Inventario).filter(
                Inventario.id_inventario == catalogo.id_inventario
            ).with_for_update().first()
            if not inventario:
                raise HTTPException(status_code=404, detail="Inventario no encontrado")
            if inventario.cantidad_disponible < it.cantidad_pedido_uds:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para {catalogo.id_catalogo}")

            precio = catalogo.precio_unidad or Decimal("0.00")
            subtotal = Decimal(precio) * int(it.cantidad_pedido_uds)

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
        db.commit()  

        # recargar el pedido completo con catálogo e inventario
        pedido_full = db.query(Pedido).options(
            joinedload(Pedido.cliente).joinedload(Cliente.usuario),
            joinedload(Pedido.detalles)
                .joinedload(DetallePedido.catalogo)
                .joinedload(Catalogo.inventario)  #  importante cargar inventario
        ).filter(Pedido.id_pedidos == pedido.id_pedidos).first()

        
        from schemas.pedido import PedidoOut
        return PedidoOut.model_validate(pedido_full, from_attributes=True)


    except Exception as e:
        db.rollback()
        print(" ERROR CREANDO PEDIDO:", e)#necesito este print para realizar seguimiento al error
        raise HTTPException(status_code=500, detail=str(e))


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

    # 3. Verificar inventario antes de entregar
    detalles = db.query(DetallePedido).filter(DetallePedido.id_pedidos == pedido_id).all()
    for detalle in detalles:
        catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == detalle.id_catalogo).first()
        if not catalogo:
            raise HTTPException(status_code=404, detail=f"Catálogo {detalle.id_catalogo} no encontrado")

        inventario = db.query(Inventario).filter(Inventario.id_inventario == catalogo.id_inventario).first()
        if not inventario:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        if inventario.cantidad_disponible < detalle.cantidad_pedido_uds:
            raise HTTPException(status_code=400, detail=f"Inventario insuficiente para {catalogo.id_catalogo}")

    # 4. Si todo OK, aplicar cambios
    pedido.estado = "entregado"
    for detalle in detalles:
        catalogo = db.query(Catalogo).filter(Catalogo.id_catalogo == detalle.id_catalogo).first()
        inventario = db.query(Inventario).filter(Inventario.id_inventario == catalogo.id_inventario).first()
        inventario.cantidad_disponible -= detalle.cantidad_pedido_uds
        db.add(inventario)

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return {
        "message": f"Pedido {pedido_id} entregado con éxito",
        "estado": pedido.estado
    }

# get para llevar los pedios al fronted
@router.get("/", response_model=list[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).options(
        joinedload(Pedido.detalles)
        .joinedload(DetallePedido.catalogo)
        .joinedload(Catalogo.inventario),
        joinedload(Pedido.cliente).joinedload(Cliente.usuario)
    ).all()

    # añadimos manualmente nombre_bebida para cada detalle
    for pedido in pedidos:
        for detalle in pedido.detalles:
            if detalle.catalogo and detalle.catalogo.inventario:
                detalle.nombre_bebida = detalle.catalogo.inventario.nombre_bebida


    return pedidos

@router.delete("/{id_pedidos}")
def eliminar_pedido(id_pedidos: int, db: Session = Depends(get_db)):
    db_pedidos = db.query(Pedido).filter(Pedido.id_pedidos == id_pedidos).first()
    if not db_pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    db.delete(db_pedidos)
    db.commit()
    return {"mensaje": f"Pedido con id {id_pedidos} eliminado"}
