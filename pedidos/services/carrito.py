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
                