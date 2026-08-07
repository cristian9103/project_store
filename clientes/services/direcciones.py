from django.db import transaction

from clientes.models import Direccion

@transaction.atomic
def crear_direccion(
    *,
    cliente,
    nombre,
    direccion,
    ciudad,
    departamento,
    codigo_postal="",
    es_principal=False,
):
    """
    Crea una dirección para un cliente.
    
    Reglas:
    - Si es la primera direccion del cliente, siempre será la principal.
    - Si se solicita como principal, desmarca la anterior.
    """
    
    tiene_direcciones = Direccion.objects.filter(
        cliente=cliente
    ).exists()
    
    if not tiene_direcciones:
        es_principal = True
        
    if es_principal:
        Direccion.objects.filter(
            cliente=cliente,
            es_principal=True
        ).update(
            es_principal=False
        )
        
    return Direccion.objects.create(
        cliente=cliente,
        nombre=nombre,
        direccion=direccion,
        ciudad=ciudad,
        departamento=departamento,
        codigo_postal=codigo_postal,
        es_principal=es_principal
    )
