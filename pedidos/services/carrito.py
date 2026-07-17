from .stock import validar_stock
from .calculos import actualizar_totales

from pedidos.models.detalles_pedido import DetallePedido

def agregar_producto(pedido, producto, cantidad):
    detalle = pedido.detalles_pedido.filter(
        producto=producto
    ).first()
    
    if detalle:
        validar_stock(producto, detalle.cantidad + cantidad)
        
        detalle.cantidad += cantidad
        
    else:
        
        validar_stock(producto, cantidad)
        
        detalle = DetallePedido(
            pedido=pedido,
            producto=producto,
            precio_unitario=producto.precio_venta,
            cantidad=cantidad
        )
        
    detalle.save()
    
    actualizar_totales(pedido)
    
    return detalle

def actualizar_cantidad(pedido, producto, nueva_cantidad):
    detalle = pedido.detalles_pedido.filter(
        producto=producto
    ).first()
    
    if detalle is None:
        raise ValueError("El producto no existe en el pedido.")
    
    if nueva_cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa.")
    
    if nueva_cantidad == 0:
        detalle.delete()
        actualizar_totales(pedido)
        return None
    
    validar_stock(producto, nueva_cantidad)
    
    detalle.cantidad = nueva_cantidad
    detalle.save()
    
    actualizar_totales(pedido)
    
    return detalle

def eliminar_producto(pedido, producto):
    return actualizar_cantidad(
        pedido,
        producto,
        nueva_cantidad=0
    )
    
def vaciar_carrito(pedido):
    pedido.detalles_pedido.all().delete()
    
    actualizar_totales(pedido)
    
    return pedido
                