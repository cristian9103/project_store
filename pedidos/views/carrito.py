from django.views import View
from django.shortcuts import get_object_or_404, redirect

from catalogo.forms import AgregarAlCarritoForm
from catalogo.models import Producto
from clientes.selectors import obtener_cliente

from pedidos.services import crear_pedido, agregar_producto

class AgregarAlCarritoView(View):
    
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
        
        agregar_producto(
            pedido=pedido,
            producto=producto,
            cantidad=form.cleaned_data["cantidad"],
        )
        
        return redirect(
            "catalogo:detalle_producto",
            pk=producto.pk,
        )
