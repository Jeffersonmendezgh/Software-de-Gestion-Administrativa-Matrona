from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db import get_db
from schemas.pedido import DetallePedidoReporte, PedidoReporte
from models.cliente import Cliente
from models.usuario import Usuario
from models.pedidos import Pedido
from models.inventario import Inventario
from models.catalogo import Catalogo
from models.detalle_pedido import DetallePedido
from schemas.cliente import ClienteCreate, ClienteOut
from utils.deps import get_current_user

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

#router para listar todos los pedidos del cliente con sus datos
@router.get("/mis-pedidos", response_model=list[PedidoReporte])
def obtener_mis_pedidos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    #buscar cliente asociado al usuario
    cliente = db.query(Cliente).filter(
        Cliente.id_usuarios == current_user.id_usuarios
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="cliente no encontrado")
    
    #vamos a obtener pedidos con relaciones
    pedidos = db.query(Pedido).options(
        joinedload(Pedido.detalles) #de los pedidos queremos los detalles
        .joinedload(DetallePedido.catalogo)#trae el catalogo
        .joinedload(Catalogo.inventario)#trae el inventario
    ).filter(
        Pedido.id_cliente == cliente.id_cliente#pedidos de el cliente exacto encontrado arriba
    ).all()

    resultado = []#aca se almacenara la lista
    for  p in pedidos: #iteramos cada pedido
        detalles_lista = []

        for d in p.detalles:
            detalles_lista.append({
                "nombre_cerveza": d.catalogo.inventario.nombre_bebida,
                "cantidad": d.cantidad_pedido_uds,
                "subtotal": d.subtotal
            })

        resultado.append({
            "id_pedido": p.id_pedidos,
            "fecha": p.fecha_pedido,
            "estado": "entregado" if getattr(p, "entregado", False)else "pendiente",
            "total": p.total_pedido,
            "detalles": detalles_lista
        })
    return resultado

#filter() decide QUÉ filas vienen de la BD
#joinedload() decide QUÉ relaciones se cargan junto a esas filas
