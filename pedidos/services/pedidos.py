from pedidos.models.pedidos import Pedido, EstadoPedido
from .calculos import ZERO, actualizar_totales
from .stock import validar_stock, descontar_stock
from pedidos.exceptions import PedidoVacioError, EstadoPedidoInvalidoError

from django.db import transaction

def crear_pedido(cliente):
    pedido = Pedido.objects.filter(
        cliente=cliente,
        estado=EstadoPedido.PENDIENTE
    ).first()
    
    if pedido:
        return pedido
    
    return Pedido.objects.create(
        cliente=cliente,
        estado=EstadoPedido.PENDIENTE,
        subtotal=ZERO,
        costo_envio=ZERO,
        descuento = ZERO,
        total=ZERO,
    ) 
    
def confirmar_pedido(pedido):
    
    with transaction.atomic():
        
        if not pedido.detalles_pedido.exists():
            raise PedidoVacioError("El pedido no tiene productos.")
        
        for detalle in pedido.detalles_pedido.select_related("producto"):
            validar_stock(
                detalle.producto,
                detalle.cantidad
            )
            
        for detalle in pedido.detalles_pedido.select_related("producto"):
            descontar_stock(
                detalle.producto,
                detalle.cantidad
            )
            
        actualizar_totales(pedido)
        
        if pedido.estado != EstadoPedido.PENDIENTE:
            raise EstadoPedidoInvalidoError("Solo los pedidos pendientes pueden confirmarse.")
        
        pedido.estado = EstadoPedido.PREPARACION
        
        pedido.save(
            update_fields=[
                "estado",
                "subtotal",
                "total"
            ]
        )
        
        return pedido
