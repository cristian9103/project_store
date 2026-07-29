from django.db import transaction

from usuarios.models import Usuario
from clientes.models import Cliente

@transaction.atomic
def registrar_usuario(
    *,
    email,
    password,
    first_name,
    last_name,
    documento,
    telefono,
):
    usuario = Usuario.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    
    cliente = Cliente.objects.create(
        usuario=usuario,
        documento=documento,
        telefono=telefono,
    )
    
    return cliente
