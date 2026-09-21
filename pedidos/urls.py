from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("carrito/", views.carrito_view, name="carrito"),
    path("carrito/agregar/<int:pk>/", views.agregar_producto, name="agregar_producto"),
    path("carrito/actualizar/<int:detalle_id>/", views.actualizar_cantidad, name="actualizar_cantidad"),
    path("carrito/vaciar/", views.vaciar_carrito, name="vaciar_carrito"),
    path("confirmar/", views.confirmar_pedido, name="confirmar_pedido"),
    path("checkout/", views.checkout_view, name="checkout",),
    path("checkout/exito/<int:pk>/", views.checkout_exito, name="checkout_exito"),
    path("mis-pedidos/", views.historial_view, name="historial"),
    path("mis-pedidos/<int:pk>/", views.detalle_view, name="detalle"),
    path("mis-pedidos/<int:pk>/cancelar/", views.cancelar_view, name="cancelar"),
    path("mis-pedidos/<int:pk>/pago/confirmar", views.confirmar_pago, name="confirmar_pago"),
    path("mis-pedidos/<int:pk>/pago/iniciar/", views.iniciar_pago, name="iniciar_pago"),
    path("mis-pedidos/<int:pk>/pago/", views.pago, name="pago"),
]