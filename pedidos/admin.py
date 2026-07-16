from django.contrib import admin

from pedidos.models.detalles_pedido import DetallePedido
from pedidos.models.pedidos import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "fecha",
        "estado",
        "subtotal",
        "costo_envio",
        "descuento",
        "total",
    )
    
    search_fields = (
        "fecha",
        "estado",
    )
    
    list_filter = (
        "fecha",
        "estado",
    )
    
    ordering = ("fecha",)
    
    list_select_related = ("cliente",)
    
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = (
        "pedido",
        "producto",
        "precio_unitario",
        "cantidad",
        "subtotal",
        "fecha_creacion",
    )
    
    search_fields = (
        "pedido__pk",
        "producto__sku",
        "fecha_creacion",
    )
    
    list_filter = (
        "pedido",
        "producto",
        "fecha_creacion",
    )
    
    ordering = ("fecha_creacion",)
    
    list_select_related = ("pedido", "producto",)
