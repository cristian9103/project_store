from django.urls import path

from usuarios.views import (
    UsuarioLoginView, 
    UsuarioLogoutView,
    RegistroView
)

app_name = "usuarios"

urlpatterns = [
    path("login/", UsuarioLoginView.as_view(), name="login"),
    path("logout/", UsuarioLogoutView.as_view(), name="logout"),
    path("registro/", RegistroView.as_view(), name="registro"),
]
