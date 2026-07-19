from django.db.models import F
from pedidos.exceptions import StockInsuficienteError

def validar_stock(producto, cantidad):
    if cantidad > producto.stock:
        raise StockInsuficienteError("No hay stock suficiente.")
    
    return True
    
def descontar_stock(producto, cantidad):
    validar_stock(producto, cantidad)
    
    producto.stock = F("stock") - cantidad
    producto.save(update_fields=["stock"])
    
    producto.refresh_from_db(fields=["stock"])
    
    return producto
    