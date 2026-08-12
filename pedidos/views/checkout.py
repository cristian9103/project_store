from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from clientes.selectors import obtener_cliente
from pedidos.services import crear_pedido

class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request):
        cliente = obtener_cliente(request.user)
        
        pedido = crear_pedido(cliente)
        
        return render(
            request,
            "pedidos/checkout/checkout.html",
            {
                "pedido": pedido,
            },
        )

checkout = CheckoutView.as_view()
