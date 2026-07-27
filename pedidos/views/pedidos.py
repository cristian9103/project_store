from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from clientes.selectors import obtener_cliente
from pedidos.selectors import obtener_pedido_pendiente
from pedidos.services import confirmar_pedido
from pedidos.exceptions import (
    PedidoVacioError,
    EstadoPedidoInvalidoError,
    StockInsuficienteError,
)

class ConfirmarPedidoView(LoginRequiredMixin, View):
    
    def post(self, request):
        cliente = obtener_cliente(request.user)
        pedido = obtener_pedido_pendiente(cliente)
        
        if pedido is None:
            messages.error(
                request,
                "No existe un pedido pendiente."
            )
            
            return redirect("pedidos:carrito")
        
        try:
            confirmar_pedido(pedido)
        except (
            PedidoVacioError,
            EstadoPedidoInvalidoError,
            StockInsuficienteError,
        ) as error:
            messages.error(
                request,
                str(error)
            )
            
            return redirect("pedidos:carrito")
        
        messages.success(
            request,
            "Pedido confirmado correctamente."
        )
        
        return redirect("pedidos:carrito")
