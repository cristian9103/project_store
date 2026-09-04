from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

class DetallePedidoView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        return HttpResponse("Detalle del pedido")
    
detalle = DetallePedidoView.as_view()
