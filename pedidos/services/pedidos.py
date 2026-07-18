from pedidos.models.pedidos import Pedido, EstadoPedido
from .calculos import ZERO

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
