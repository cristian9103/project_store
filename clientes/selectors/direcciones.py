from django.shortcuts import get_object_or_404

from clientes.models import Direccion

def listar_direcciones(cliente):
    return Direccion.objects.filter(
        cliente=cliente
    )
    
def obtener_direccion(direccion_id, cliente):
    return get_object_or_404(
        Direccion,
        pk=direccion_id,
        cliente=cliente
    )
    
def obtener_direccion_principal(cliente):
    return Direccion.objects.filter(
        cliente=cliente,
        es_principal=True,
    ).first()
