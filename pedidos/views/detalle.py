from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from clientes.selectors import obtener_cliente
from pedidos.models import Pedido, EstadoPago, Pago

class DetallePedidoView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/detalle/detalle.html"
    context_object_name = "pedido"
    
    def get_queryset(self):
        cliente = obtener_cliente(self.request.user)
        
        return Pedido.objects.filter(
            cliente=cliente
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["pago_pendiente"] = Pago.objects.filter(
            pedido=self.object,
            estado=EstadoPago.PENDIENTE,
        ).first()
        
        return context
       
detalle = DetallePedidoView.as_view()
