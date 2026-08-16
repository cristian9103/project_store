from pedidos.exceptions import EstadoPedidoInvalidoError
from pedidos.models import EstadoPedido


def iniciar_pago(pedido):
    if pedido.estado != EstadoPedido.PENDIENTE:
        raise EstadoPedidoInvalidoError(
            "El pedido no está en un estado válido para iniciar el pago."
        )
    
    return True
