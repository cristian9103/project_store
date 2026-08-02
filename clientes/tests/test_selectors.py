from django.http import Http404

from .base import BaseTestCase

from clientes.selectors import obtener_cliente
from usuarios.models import Usuario
from clientes.models import Cliente

class ObtenerClienteTest(BaseTestCase):
    
    def test_obtener_cliente_devuelve_cliente(self):
        
        cliente = obtener_cliente(
            self.usuario
        )
        
        self.assertEqual(
            cliente,
            self.cliente
        )
        
    def test_obtener_cliente_devuelve_el_cliente_correcto(self):
        
        otro_usuario = Usuario.objects.create_user(
            email="otro@test.com",
            password="123456789",
            first_name="Otro",
            last_name="Usuario"
        )
        
        otro_cliente = Cliente.objects.create(
            usuario=otro_usuario,
            documento="987654321",
            telefono="3111234567"
        )
        
        cliente = obtener_cliente(
            self.usuario
        )
        
        self.assertEqual(
            cliente,
            self.cliente
        )
        
        self.assertNotEqual(
            cliente,
            otro_cliente
        )
        
    def test_obtener_cliente_usuario_sin_cliente(self):
        
        usuario = Usuario.objects.create_user(
            email="sincliente@test.com",
            password="123456789",
            first_name="Sin",
            last_name="Cliente",
        )
        
        with self.assertRaises(Http404):
            obtener_cliente(usuario)
            
    def test_obtener_cliente_usa_una_consulta(self):
        
        with self.assertNumQueries(1):
            
            cliente = obtener_cliente(
                self.usuario
            )
            
            cliente.usuario.first_name
