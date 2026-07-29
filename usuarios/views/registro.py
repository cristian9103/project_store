from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from usuarios.forms import RegistroForm
from usuarios.services import registrar_usuario

class RegistroView(FormView):
    
    template_name = "usuarios/registro.html"
    
    form_class = RegistroForm
    
    success_url = reverse_lazy("catalogo:lista_productos")
    
    def form_valid(self, form):
        
        cliente = registrar_usuario(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            documento=form.cleaned_data["documento"],
            telefono=form.cleaned_data["telefono"],
        )
        
        login(
            self.request,
            cliente.usuario
        )
        
        return super().form_valid(form)
