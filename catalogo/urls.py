from django.urls import path

from .views import (
    ProductoListView,
    ProductoDetailView,
)

urlpatterns = [
    path("", ProductoListView.as_view(), name="lista_productos"),
    path("<int:pk>/", ProductoDetailView.as_view(), name="detalle_producto"),
]