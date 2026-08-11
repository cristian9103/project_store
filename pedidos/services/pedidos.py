from pedidos.models.pedidos import Pedido, EstadoPedido
from .calculos import ZERO, actualizar_totales
from .stock import validar_stock, descontar_stock
from pedidos.exceptions import (
    PedidoVacioError, 
    EstadoPedidoInvalidoError,
    PedidoSinDireccionError,
)

from django.db import transaction, IntegrityError

def crear_pedido(cliente):
    pedido = Pedido.objects.filter(
        cliente=cliente,
        estado=EstadoPedido.PENDIENTE
    ).first()
    
    if pedido:
        return pedido
    
    try:
        with transaction.atomic():
            return Pedido.objects.create(
                cliente=cliente,
                estado=EstadoPedido.PENDIENTE,
                subtotal=ZERO,
                costo_envio=ZERO,
                descuento = ZERO,
                total=ZERO,
            )
            
    except IntegrityError as error:
        
        constraint_name = getattr(
            getattr(error.__cause__, "diag", None),
            "constraint_name",
            None
        )
        
        if constraint_name != "unique_pedido_pendiente_por_cliente":
            raise
        
        return Pedido.objects.get(
            cliente=cliente,
            estado=EstadoPedido.PENDIENTE
        )
    
def confirmar_pedido(pedido):
    
    with transaction.atomic():
        
        if pedido.estado != EstadoPedido.PENDIENTE:
            raise EstadoPedidoInvalidoError(
                "Solo los pedidos pendientes pueden confirmarse."
            )
            
        if pedido.direccion_envio is None:
            raise PedidoSinDireccionError(
                "El pedido necesita una dirección de envío."
            )
        
        detalles = list(
            pedido.detalles_pedido
            .select_related("producto")
            .select_for_update(
                of=("producto",)
            )
        )
        
        if not detalles:
            raise PedidoVacioError(
                "El pedido no tiene productos."
            )
        
        for detalle in detalles:
            validar_stock(
                detalle.producto,
                detalle.cantidad
            )
            
        for detalle in detalles:
            descontar_stock(
                detalle.producto,
                detalle.cantidad
            )
            
        actualizar_totales(pedido)
        
        pedido.estado = EstadoPedido.PREPARACION
        
        pedido.save(
            update_fields=[
                "estado",
                "subtotal",
                "total"
            ]
        )
        
        return pedido
