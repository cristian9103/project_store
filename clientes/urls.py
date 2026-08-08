from django.urls import path

from clientes import views

app_name = "clientes"

urlpatterns = [
    path("direcciones/nueva/", views.crear_direccion, name="crear_direccion",),
]