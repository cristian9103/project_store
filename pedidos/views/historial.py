from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from clientes.selectors import obtener_cliente
from pedidos.models import Pedido

class HistorialPedidosView(LoginRequiredMixin, View):
    
    def get(self, request):
        cliente = obtener_cliente(request.user)
        
        pedidos = Pedido.objects.filter(
            cliente=cliente
        )
        
        return render(
            request,
            "pedidos/historial/historial.html",
            {
                "pedidos": pedidos
            },
        )
    
historial = HistorialPedidosView.as_view()
