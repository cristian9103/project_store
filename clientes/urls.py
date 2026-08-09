from django.urls import path

from clientes import views

app_name = "clientes"

urlpatterns = [
    path("direcciones/nueva/", views.crear_direccion, name="crear_direccion",),
    path("direcciones/", views.lista_direcciones, name="lista_direcciones",),
    path("direcciones/<int:pk>/", views.detalle_direccion, name="detalle_direccion",),
]