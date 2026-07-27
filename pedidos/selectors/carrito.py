from pedidos.models import Pedido, EstadoPedido

def obtener_pedido_pendiente(cliente):
    return (
        Pedido.objects
        .filter(
            cliente=cliente,
            estado=EstadoPedido.PENDIENTE,
        )
        .prefetch_related(
            "detalles_pedido__producto",
        )
        .first()
    )
