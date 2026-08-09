from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from clientes.forms import DireccionForm
from clientes.selectors import obtener_cliente
from clientes.services import crear_direccion as crear_direccion_service

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
        
crear_direccion = CrearDireccionView.as_view()
