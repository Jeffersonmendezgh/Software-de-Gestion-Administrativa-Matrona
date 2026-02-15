from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from db import get_db
from models.pedidos import Pedido
from models.detalle_pedido import DetallePedido
from models.catalogo import Catalogo
from models.cliente import Cliente
from models.usuario import Usuario
from models.inventario import Inventario
from schemas.contabilidad import VentaHistorialResponse, IngresosPorProductoResponse
router = APIRouter(prefix="/contabilidad", tags=["Contabilidad"])

#historial de ventas
@router.get("/historial", response_model=List[VentaHistorialResponse])
def obtener_historial_ventas(db:Session = Depends(get_db)):
    resultados = (
        db.query(
            Pedido.id_pedidos.label("id_pedidos"),
            Inventario.nombre_bebida.label("nombre_bebida"),
            DetallePedido.cantidad_pedido_uds.label("cantidad"),
            Pedido.fecha_pedido,
            (func.concat(Usuario.nombre, " ", Usuario.apellido)).label("nombre_cliente"),
            DetallePedido.subtotal.label("total_venta")
        )
        .join(Cliente, Pedido.id_cliente == Cliente.id_cliente)#para saber quien hizo el pedido
        .join(Usuario, Cliente.id_usuarios == Usuario.id_usuarios)#obtener el nombre delcliente
        .join(DetallePedido, Pedido.id_pedidos == DetallePedido.id_pedidos)#para saber que pidio
        .join(Catalogo, DetallePedido.id_catalogo == Catalogo.id_catalogo)#para conocer el catalogo product
        .join(Inventario, Catalogo.id_inventario == Inventario.id_inventario)#traer nombre bebida
        .all()
    )
    return resultados

#router para calcular el ingreso total por productos
@router.get("/ingresos", response_model=List[IngresosPorProductoResponse])
def obtener_ingresos_por_producto(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            Inventario.nombre_bebida.label("nombre_bebida"),
            func.sum(DetallePedido.subtotal).label("total_ingresos")#fun para sumar todo lo que va de ingresoso y mostrarlo
        )
        .join(Catalogo, Catalogo.id_catalogo == DetallePedido.id_catalogo)
        .join(Inventario, Catalogo.id_inventario == Inventario.id_inventario)
        .group_by(Inventario.nombre_bebida)
        .all()
    )
    return resultados