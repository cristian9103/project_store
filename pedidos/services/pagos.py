from pedidos.exceptions import (
    EstadoPedidoInvalidoError,
    PedidoVacioError,
    PedidoSinDireccionError,
    EstadoPagoInvalidoError,
)
from pedidos.models import (
    EstadoPedido,
    EstadoPago,
    Pago,
)
from pedidos.services import confirmar_pedido

from django.db import transaction

def iniciar_pago(pedido):
    if pedido.estado != EstadoPedido.PENDIENTE:
        raise EstadoPedidoInvalidoError(
            "El pedido no está en un estado válido para iniciar el pago."
        )
        
    if not pedido.detalles_pedido.exists():
        raise PedidoVacioError(
            "El pedido no tiene productos."
        )
        
    if pedido.direccion_envio_id is None:
        raise PedidoSinDireccionError(
            "El pedido necesita una dirección de envío."
        )
        
    pago_pendiente = Pago.objects.filter(
        pedido=pedido,
        estado=EstadoPago.PENDIENTE,
    ).first()
    
    if pago_pendiente:
        return pago_pendiente
    
    pago_aprobado = Pago.objects.filter(
        pedido=pedido,
        estado=EstadoPago.APROBADO,
    ).first()
        
    if pago_aprobado:
        raise EstadoPagoInvalidoError(
            "El pedido ya tiene un pago aprobado."
        )
    
    return Pago.objects.create(
        pedido=pedido,
        estado=EstadoPago.PENDIENTE,
    )
    
def procesar_pago(pago, aprobado):
    if pago.estado != EstadoPago.PENDIENTE:
        raise EstadoPagoInvalidoError(
            "El pago no está pendiente."
        )
        
    if aprobado:
        pago.estado = EstadoPago.APROBADO
        pago.save(update_fields=["estado"])
        return True
    
    pago.estado = EstadoPago.RECHAZADO
    pago.save(update_fields=["estado"])
    return False

def aplicar_pago_aprobado(pago):
    if pago.estado != EstadoPago.APROBADO:
        raise EstadoPagoInvalidoError(
            "El pago debe estar aprobado."
        )
        
    pedido = pago.pedido
    
    if pedido.estado != EstadoPedido.PENDIENTE:
        raise EstadoPedidoInvalidoError(
            "El pedido debe estar pendiente."
        )
        
    confirmar_pedido(pedido)
    
    return True

def confirmar_pago(pago, aprobado):
    with transaction.atomic():
        resultado = procesar_pago(
            pago=pago,
            aprobado=aprobado,
        )
        
        if resultado:
            aplicar_pago_aprobado(pago)
            
        return resultado
