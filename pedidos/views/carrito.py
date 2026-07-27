from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from catalogo.forms import AgregarAlCarritoForm
from catalogo.models import Producto
from clientes.selectors import obtener_cliente

from pedidos.services import (
    crear_pedido, 
    agregar_producto, 
    actualizar_cantidad,
    vaciar_carrito,
)
from pedidos.forms import ActualizarCantidadForm
from pedidos.selectors import obtener_pedido_pendiente
from pedidos.models import DetallePedido
from pedidos.exceptions import (
    StockInsuficienteError,
    CantidadInvalidaError,
    ProductoNoExisteEnPedidoError
)

class AgregarAlCarritoView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        producto = get_object_or_404(
            Producto.objects.disponibles(),
            pk=pk,
        )
        
        form = AgregarAlCarritoForm(
            request.POST,
            producto=producto
        )
        
        if not form.is_valid():
            return redirect(
                "catalogo:detalle_producto",
                pk=producto.pk,
            )
            
        cliente = obtener_cliente(request.user)
        
        pedido = crear_pedido(cliente)
        
        try:
        
            agregar_producto(
                pedido=pedido,
                producto=producto,
                cantidad=form.cleaned_data["cantidad"],
            )
            
            messages.success(
                request,
                "Producto agregado al carrito."
            )
            
            return redirect("pedidos:carrito")
        
        except (
            StockInsuficienteError,
            CantidadInvalidaError,
            ProductoNoExisteEnPedidoError,
        ) as error:
            
            messages.error(
                request,
                str(error)
            )
        
            return redirect(
                "catalogo:detalle_producto",
                pk=producto.pk,
            )
      
class CarritoDetailView(LoginRequiredMixin, TemplateView):
    
    template_name = "pedidos/carrito.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cliente = obtener_cliente(self.request.user)
        
        pedido = obtener_pedido_pendiente(cliente)
        
        context["pedido"] = pedido
        
        return context
    
class ActualizarCantidadView(LoginRequiredMixin, View):
    
    def post(self, request, detalle_id):
        
        detalle = get_object_or_404(
            DetallePedido.objects.select_related(
                "pedido",
                "producto",
            ),
            pk=detalle_id,
        )
        
        form = ActualizarCantidadForm(request.POST)
        
        if not form.is_valid():
            return redirect("pedidos:carrito")
        
        try:
            actualizar_cantidad(
                pedido=detalle.pedido,
                producto=detalle.producto,
                nueva_cantidad=form.cleaned_data["cantidad"],
            )
            
            messages.success(
                request,
                "Cantidad actualizada."
            )
        except (
            StockInsuficienteError,
            CantidadInvalidaError,
            ProductoNoExisteEnPedidoError,
        ) as error:
            
            messages.error(
                request,
                str(error),
            )
            
        return redirect(
            "pedidos:carrito"
        )
        
class VaciarCarritoView(LoginRequiredMixin, View):
    
    def post(self, request):
        cliente = obtener_cliente(request.user)
        pedido = obtener_pedido_pendiente(cliente)
        
        if pedido:
            vaciar_carrito(pedido)
            
            messages.success(
                request,
                "El carrito se vació correctamente."
            )
            
        return redirect("pedidos:carrito")
