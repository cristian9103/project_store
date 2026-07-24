from django.shortcuts import get_object_or_404

from clientes.models import Cliente

def obtener_cliente(usuario):
    return get_object_or_404(
        Cliente.objects.select_related("usuario"),
        usuario=usuario,
    )