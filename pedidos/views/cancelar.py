from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from clientes.selectors import obtener_cliente
from pedidos.models import Pedido
from pedidos.services import cancelar_pedido

class CancelarPedidoView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        pedido = get_object_or_404(
            Pedido,
            pk=pk,
            cliente=cliente,
        )
        
        cancelar_pedido(pedido)
        
        return redirect(
            "pedidos:detalle",
            pk=pedido.pk,
        )
        
cancelar = CancelarPedidoView.as_view()
