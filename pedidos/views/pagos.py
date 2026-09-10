from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from clientes.selectors import obtener_cliente
from pedidos.models import Pedido, EstadoPago
from pedidos.services.pagos import confirmar_pago as confirmar_pago_service

class ConfirmarPagoView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        pedido = get_object_or_404(
            Pedido,
            pk=pk,
            cliente=cliente,
        )
        
        pago = pedido.pagos.get(
            estado=EstadoPago.PENDIENTE,
        )
        
        confirmar_pago_service(
            pago,
            aprobado=True,
        )
        
        return redirect(
            "pedidos:detalle",
            pk=pedido.pk,
        )
        
confirmar_pago = ConfirmarPagoView.as_view()
