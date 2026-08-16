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
        
    pago = Pago.objects.filter(
        pedido=pedido,
    ).first()
    
    if pago:
        if pago.estado == EstadoPago.PENDIENTE:
            return pago
        
        if pago.estado == EstadoPago.APROBADO:
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
