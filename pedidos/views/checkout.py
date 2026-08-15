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
    confirmar_pedido,
)
from pedidos.forms import CheckoutForm
from pedidos.exceptions import (
    PedidoSinDireccionError,
    PedidoVacioError,
    StockInsuficienteError,
)

class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request):
        cliente = obtener_cliente(request.user)
        
        pedido = crear_pedido(cliente)
        direcciones = listar_direcciones(cliente)
        
        form = CheckoutForm()
        
        return render(
            request,
            "pedidos/checkout/checkout.html",
            {
                "pedido": pedido,
                "direcciones": direcciones,
                "form": form,
            },
        )
        
    def post(self, request):
        cliente = obtener_cliente(request.user)
        
        pedido = crear_pedido(cliente)
        
        accion = request.POST.get("accion")
        
        if accion == "confirmar":
            try:
                confirmar_pedido(pedido)
                
            except (
                PedidoSinDireccionError,
                PedidoVacioError,
                StockInsuficienteError,
            ) as error:
                
                return render(
                    request,
                    "pedidos/checkout/checkout.html",
                    {
                        "pedido": pedido,
                        "direcciones": listar_direcciones(cliente),
                        "form": CheckoutForm(),
                        "error": str(error),
                    },
                )
            
            return redirect("pedidos:checkout")
        
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            direccion_id = form.cleaned_data["direccion_id"]
            
            direccion = obtener_direccion(
                direccion_id=direccion_id,
                cliente=cliente
            )
            
            asignar_direccion_pedido(
                pedido=pedido,
                direccion=direccion,
            )
            
            return redirect("pedidos:checkout")
        
        return render(
            request,
            "pedidos/checkout/checkout.html",
            {
                "pedido": pedido,
                "direcciones": listar_direcciones(cliente),
                "form": form,
            },
        )


checkout = CheckoutView.as_view()
