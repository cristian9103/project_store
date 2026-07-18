class CarritoError(Exception):
    """Excepción base para errores en carrito."""
    pass

class ProductoNoExisteEnPedidoError(CarritoError):
    """No existe el producto en el pedido buscado."""
    pass

class CantidadInvalidaError(CarritoError):
    """La cantidad ingresada es una cantidad inválida o negativa"""
    pass