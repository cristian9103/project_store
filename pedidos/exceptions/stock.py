class StockError(Exception):
    """Excepción base para errores de stock."""
    pass

class StockInsuficienteError(StockError):
    """No hay stock suficiente."""
    pass