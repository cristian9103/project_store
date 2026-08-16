from pedidos.exceptions import (
    EstadoPedidoInvalidoError,
    PedidoVacioError,
    PedidoSinDireccionError,
)
from pedidos.models import EstadoPedido


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
    
    return True
