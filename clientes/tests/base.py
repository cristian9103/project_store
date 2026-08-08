from django.test import TestCase

from usuarios.models import Usuario
from clientes.models import Cliente, Direccion

class BaseTestCase(TestCase):
    
    def setUp(self):
        
        self.usuario = Usuario.objects.create_user(
            email="cliente@test.com",
            password="123456789",
            first_name="Cristian",
            last_name="Ramirez",
        )
        
        self.otro_usuario = Usuario.objects.create_user(
            email="otro_cliente@test.com",
            password="1234567899",
            first_name="Camilo",
            last_name="Ramirez",
        )
        
        self.cliente = Cliente.objects.create(
            usuario=self.usuario,
            documento="123456789",
            telefono="3001234567",
        )
        
    def crear_direccion(
        self,
        nombre="Casa",
        direccion="Carrera 10 # 20-30",
        ciudad="Medellín",
        departamento="Antioquia",
        codigo_postal="050001",
        es_principal=False
    ):
        return Direccion.objects.create(
            cliente=self.cliente,
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            departamento=departamento,
            codigo_postal=codigo_postal,
            es_principal=es_principal,
        )
