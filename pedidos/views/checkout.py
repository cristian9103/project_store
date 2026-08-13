from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from clientes.selectors import (
    obtener_cliente, 
    listar_direcciones,
    obtener_direccion,
)
from pedidos.services import (
    crear_pedido,
    asignar_direccion_pedido,
)
from pedidos.forms import CheckoutForm

class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request):
        cliente = obtener_cliente(request.user)
        
        pedido = crear_pedido(cliente)
        direcciones = listar_direcciones(cliente)
        
        return render(
            request,
            "pedidos/checkout/checkout.html",
            {
                "pedido": pedido,
                "direcciones": direcciones,
            },
        )
        
    def post(self, request):
        cliente = obtener_cliente(request.user)
        
        pedido = crear_pedido(cliente)
        
        direccion_id = request.POST.get("direccion_id")
        
        direccion = obtener_direccion(
            direccion_id=direccion_id,
            cliente=cliente
        )
        
        asignar_direccion_pedido(
            pedido=pedido,
            direccion=direccion,
        )
        
        return redirect("pedidos:checkout")


checkout = CheckoutView.as_view()
