from decimal import Decimal
from django.db.models import Sum

ZERO = Decimal("0.00")

def calcular_subtotal(pedido):
    resultado = pedido.detalles_pedido.aggregate(
        subtotal=Sum("subtotal")
    )
    
    return resultado["subtotal"] or ZERO

def calcular_total(pedido, subtotal=None):
    if subtotal is None:
        subtotal = calcular_subtotal(pedido)
    return subtotal + pedido.costo_envio - pedido.descuento

def actualizar_totales(pedido):
    subtotal = calcular_subtotal(pedido)
    total = calcular_total(pedido, subtotal)
    
    pedido.subtotal = subtotal
    pedido.total = total
    
    pedido.save(update_fields=["subtotal", "total"])
    
    return pedido