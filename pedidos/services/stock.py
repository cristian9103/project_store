class StockInsuficiente(Exception):
    pass

def validar_stock(producto, cantidad):
    if cantidad > producto.stock:
        raise StockInsuficiente("La cantidad en el stock actual es menor a la deseada.")