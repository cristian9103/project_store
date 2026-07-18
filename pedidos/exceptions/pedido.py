class PedidoError(Exception):
    """Excepción base para errores en pedido"""
    pass

class PedidoVacioError(PedidoError):
    """El pedido se encuentra vacío"""
    pass

class EstadoPedidoInvalidoError(PedidoError):
    """El pedido no se encuentra en estado pendiente"""
    pass