from clientes.models import Direccion

def obtener_direcciones_pedido(pedido):
    return Direccion.objects.filter(
        cliente_id=pedido.cliente_id
    )
