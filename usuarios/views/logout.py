from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class UsuarioLogoutView(LogoutView):
    next_page = reverse_lazy("usuarios:login")
