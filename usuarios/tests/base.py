from django.test import TestCase

from usuarios.models import Usuario
from clientes.models import Cliente

class BaseTestCase(TestCase):
    
    def crear_usuario(
        self,
        email="usuario@test.com",
        password="TestPassword123!",
        first_name="Cristian",
        last_name="Ramirez",
    ):
        usuario = Usuario.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        return usuario
    
    def crear_cliente(
        self,
        usuario=None,
        documento="123456789",
        telefono="3001234567",
    ):
        if usuario is None:
            usuario = self.crear_usuario()
            
        cliente = Cliente.objects.create(
            usuario=usuario,
            documento=documento,
            telefono=telefono,
        )
        
        return cliente
    
    def datos_registro(self, **overrides):
        datos = {
            "email": "nuevo@test.com",
            "password": "TestPassword123!",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "documento": "111111111",
            "telefono": "3001111111",
        }
        
        datos.update(overrides)
        
        return datos
