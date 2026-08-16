from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.detail import DetailView

from clientes.selectors import (
    obtener_cliente, 
    listar_direcciones,
    obtener_direccion,
)
from pedidos.services import (
    crear_pedido,
    asignar_direccion_pedido,
    confirmar_pedido,
    obtener_pedido_pendiente,
)
from pedidos.forms import CheckoutForm
from pedidos.exceptions import (
    PedidoSinDireccionError,
    PedidoVacioError,
    StockInsuficienteError,
)
from pedidos.models import Pedido, EstadoPedido

class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request):
        cliente = obtener_cliente(request.user)
        
        pedido = obtener_pedido_pendiente(cliente)
        
        if pedido is None:
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
        
        pedido = obtener_pedido_pendiente(cliente)
        
        if pedido is None:
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
            
            return redirect(
                "pedidos:checkout_exito",
                pk=pedido.pk,
            )
        
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
        
class CheckoutExitoView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/checkout/exito.html"
    context_object_name = "pedido"
    
    def get_queryset(self):
        cliente = obtener_cliente(self.request.user)
        
        return Pedido.objects.filter(
            cliente=cliente,
            estado=EstadoPedido.PREPARACION,
        )


checkout = CheckoutView.as_view()
checkout_exito = CheckoutExitoView.as_view()
