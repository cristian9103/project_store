from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from clientes.selectors import obtener_cliente
from pedidos.models import Pedido
from pedidos.services.pagos import (
    confirmar_pago as confirmar_pago_service,
    iniciar_pago as iniciar_pago_service,
)
from pedidos.exceptions import EstadoPagoInvalidoError

class ConfirmarPagoView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        pedido = get_object_or_404(
            Pedido,
            pk=pk,
            cliente=cliente,
        )
        
        pago = pedido.pagos.first()
        
        if pago is None:
            messages.error(
                request,
                "El pedido no tiene un pago.",
            )
            
            return redirect(
                "pedidos:detalle",
                pk=pedido.pk,
            )
        
        try:
            confirmar_pago_service(
                pago,
                aprobado=True,
            )
        except EstadoPagoInvalidoError as error:
            messages.error(
                request,
                str(error),
            )
        
        return redirect(
            "pedidos:detalle",
            pk=pedido.pk,
        )
        
class IniciarPagoView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        pedido = get_object_or_404(
            Pedido,
            pk=pk,
            cliente=cliente,
        )
        
        iniciar_pago_service(pedido)
        
        return redirect(
            "pedidos:detalle",
            pk=pedido.pk,
        )
        
confirmar_pago = ConfirmarPagoView.as_view()
iniciar_pago = IniciarPagoView.as_view()
