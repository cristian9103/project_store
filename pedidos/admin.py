from django.contrib import admin, messages
from django.db import transaction

from pedidos.models import Pedido, DetallePedido, EstadoPedido
from pedidos.services import enviar_pedido
from pedidos.exceptions import EstadoPedidoInvalidoError

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
    
    @admin.action(description="Enviar Pedidos seleccionados")
    def enviar_pedidos(self, request, queryset):
        pedidos = list(queryset)
        
        if any(
            pedido.estado != EstadoPedido.PREPARACION
            for pedido in pedidos
        ):
            self.message_user(
                request,
                "Tdoso los pedidos seleccionados deben estar en preparación.",
                level=messages.ERROR,
            )
            return
        
        with transaction.atomic():
            for pedido in pedidos:
                enviar_pedido(pedido)
                
        self.message_user(
            request,
            "Los pedidos seleccionados fueron enviado correctamente.",
            level=messages.SUCCESS,
        )
        
    actions = (
        "enviar_pedidos",
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
