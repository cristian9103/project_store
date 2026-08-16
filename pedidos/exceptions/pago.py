class PagoError(Exception):
    pass

class EstadoPagoInvalidoError(PagoError):
    pass