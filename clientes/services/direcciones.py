from django.db import transaction

from clientes.models import Direccion

@transaction.atomic
def establecer_principal(direccion):
    
    Direccion.objects.filter(
        cliente=direccion.cliente,
        es_principal=True,
    ).exclude(
        pk=direccion.pk,
    ).update(
        es_principal=False
    )
    
    if not direccion.es_principal:
        direccion.es_principal = True
        direccion.save(
            update_fields=["es_principal"]
        )
        
    return direccion

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
        
    direccion_obj = Direccion.objects.create(
        cliente=cliente,
        nombre=nombre,
        direccion=direccion,
        ciudad=ciudad,
        departamento=departamento,
        codigo_postal=codigo_postal,
        es_principal=False,
    )
    
    if not tiene_direcciones or es_principal:
        establecer_principal(direccion_obj)
        
    return direccion_obj

@transaction.atomic
def actualizar_direccion(
    direccion,
    *,
    nombre,
    direccion_texto,
    ciudad,
    departamento,
    codigo_postal="",
    es_principal=False,
):
    direccion.nombre = nombre
    direccion.direccion = direccion_texto
    direccion.ciudad = ciudad
    direccion.departamento = departamento
    direccion.codigo_postal = codigo_postal
    
    if es_principal:
        establecer_principal(direccion)
    else:
        direccion.es_principal = False
    
    direccion.save(
        update_fields=[
            "nombre",
            "direccion",
            "ciudad",
            "departamento",
            "codigo_postal",
            "es_principal",
        ]
    )
        
    return direccion

@transaction.atomic
def eliminar_direccion(direccion):
    
    era_principal = direccion.es_principal
    cliente = direccion.cliente
    
    direccion.delete()
    
    if era_principal:
        nueva_principal = (
            Direccion.objects
            .filter(cliente=cliente)
            .order_by("fecha_creacion")
            .first()
        )
        
        if nueva_principal:
            establecer_principal(nueva_principal)
            
    return True
