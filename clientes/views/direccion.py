from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from clientes.forms import DireccionForm
from clientes.selectors import (
    obtener_cliente,
    listar_direcciones,
    obtener_direccion,
)
from clientes.services import (
    crear_direccion as crear_direccion_service,
    actualizar_direccion,
)

class CrearDireccionView(LoginRequiredMixin, View):
    
    def get(self, request):
        form = DireccionForm()
        
        return render(
            request,
            "clientes/direcciones/form.html",
            {"form": form}
        )
        
    def post(self, request):
        form = DireccionForm(request.POST)
        
        if form.is_valid():
            cliente = obtener_cliente(request.user)
            
            crear_direccion_service(
                cliente=cliente,
                **form.cleaned_data,
            )
            
            return redirect("clientes:crear_direccion")
        
        return render(
            request,
            "clientes/direcciones/form.html",
            {"form": form},
        )
        
class ListaDireccionesView(LoginRequiredMixin, View):
    
    def get(self, request):
        cliente = obtener_cliente(request.user)
        
        direcciones = listar_direcciones(cliente)
        
        return render(
            request,
            "clientes/direcciones/lista.html",
            {
                "direcciones": direcciones,
            },
        )
        
class DetalleDireccionView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        direccion = obtener_direccion(
            direccion_id=pk, 
            cliente=cliente
        )
        
        return render(
            request,
            "clientes/direcciones/detalle.html",
            {
                "direccion": direccion
            },
        )
        
class EditarDireccionView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        direccion = obtener_direccion(
            direccion_id=pk,
            cliente=cliente,
        )
        
        form = DireccionForm(instance=direccion)
        
        return render(
            request,
            "clientes/direcciones/form.html",
            {
                "form": form,
                "direccion": direccion,
            },
        )
        
    def post(self, request, pk):
        cliente = obtener_cliente(request.user)
        
        direccion = obtener_direccion(
            direccion_id=pk,
            cliente=cliente,
        )
        
        form = DireccionForm(
            request.POST,
            instance=direccion,
        )
        
        if form.is_valid():
            
            datos = form.cleaned_data.copy()
            
            datos["direccion_texto"] = datos.pop("direccion")
            
            actualizar_direccion(
                direccion=direccion,
                **datos,
            )
            
            return redirect(
                "clientes:detalle_direccion",
                pk=direccion.pk,
            )
            
        return render(
            request,
            "clientes/direcciones/form.html",
            {
                "form": form,
                "direccion": direccion,
            },
        )
        
        
crear_direccion = CrearDireccionView.as_view()
lista_direcciones = ListaDireccionesView.as_view()
detalle_direccion = DetalleDireccionView.as_view()
editar_direccion = EditarDireccionView.as_view()
