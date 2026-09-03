from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from clientes.selectors import obtener_cliente
from pedidos.models import Pedido

class HistorialPedidosView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "pedidos/historial/historial.html"
    context_object_name = "pedidos"
    paginate_by = 10
    
    def get_queryset(self):
        cliente = obtener_cliente(self.request.user)
        
        return Pedido.objects.filter(
            cliente=cliente
        )
    
historial = HistorialPedidosView.as_view()
