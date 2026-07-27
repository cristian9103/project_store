from django.urls import path

from pedidos.views import (
    AgregarAlCarritoView,
    CarritoDetailView,
    ActualizarCantidadView,
)

app_name = "pedidos"

urlpatterns = [
    path("carrito/", CarritoDetailView.as_view(), name="carrito"),
    path("carrito/agregar/<int:pk>/", AgregarAlCarritoView.as_view(), name="agregar_producto"),
    path("carrito/actualizar/<int:detalle_id>/", ActualizarCantidadView.as_view(), name="actualizar_cantidad"),
]