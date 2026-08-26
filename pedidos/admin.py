from django.contrib import admin

from pedidos.models.detalles_pedido import DetallePedido
from pedidos.models.pedidos import Pedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    
    fields = (
        "producto",
        "precio_unitario",
        "cantidad",
        "subtotal",
    )
    
    readonly_fields = (
        "producto",
        "precio_unitario",
        "cantidad",
        "subtotal",
    )
    
    extra = 0
    can_delete = False

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "estado",
        "fecha",
        "total",
    )
    
    search_fields = (
        "id",
        "cliente__documento",
    )
    
    list_filter = (
        "fecha",
        "estado",
    )
    
    list_select_related = ("cliente",)
    
    readonly_fields = (
        "cliente",
        "direccion_envio",
        "fecha",
        "estado",
        "subtotal",
        "costo_envio",
        "descuento",
        "total",
    )
    
    inlines = (
        DetallePedidoInline,
    )
    
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
        "producto__pk",
        "fecha_creacion",
    )
    
    list_filter = (
        "pedido",
        "producto",
        "fecha_creacion",
    )
    
    ordering = ("fecha_creacion",)
    
    list_select_related = (
        "pedido",
        "producto",
    )
    
    readonly_fields = (
        "pedido",
        "producto",
        "precio_unitario",
        "cantidad",
        "subtotal",
        "fecha_creacion",
    )
