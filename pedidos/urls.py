from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("carrito/", views.CarritoDetailView.as_view(), name="carrito"),
    path("carrito/agregar/<int:pk>/", views.AgregarAlCarritoView.as_view(), name="agregar_producto"),
    path("carrito/actualizar/<int:detalle_id>/", views.ActualizarCantidadView.as_view(), name="actualizar_cantidad"),
    path("carrito/vaciar/", views.VaciarCarritoView.as_view(), name="vaciar_carrito"),
    path("confirmar/", views.ConfirmarPedidoView.as_view(), name="confirmar_pedido"),
    path("checkout/", views.checkout, name="checkout",),
]