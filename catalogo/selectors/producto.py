from django.shortcuts import get_object_or_404

from catalogo.models import Producto

def buscar_productos(
    *,
    texto=None,
    categoria=None,
    marca=None
):
    queryset = Producto.objects.disponibles()
    
    if texto:
        queryset = queryset.filter(
            nombre__icontains=texto.strip()
        )
        
    if categoria:
        queryset = queryset.filter(
            categoria=categoria
        )
        
    if marca:
        queryset = queryset.filter(
            marca=marca
        )
        
    return (
        queryset
        .select_related("categoria", "marca")
        .prefetch_related("imagenes")
        .order_by("nombre")
    )
    
def obtener_producto(pk):
    queryset = (
        Producto.objects.disponibles()
        .select_related(
            "categoria",
            "marca",
        )
        .prefetch_related(
            "imagenes",
        )
    )
    
    return get_object_or_404(
        queryset,
        pk=pk
    )
    