from django.db.models import F
from pedidos.exceptions import StockInsuficienteError

def validar_stock(producto, cantidad):
    if cantidad > producto.stock:
        raise StockInsuficienteError("La cantidad en el stock actual es menor a la deseada.")
    
def descontar_stock(producto, cantidad):
    validar_stock(producto, cantidad)
    
    producto.stock = F("stock") - cantidad
    producto.save(update_fields=["stock"])
    
    producto.refresh_from_db(fields=["stock"])
    
    return producto
    