from django.http import Http404

from .base import BaseTestCase

from clientes.selectors import (
    obtener_cliente,
    listar_direcciones,
    obtener_direccion,
    obtener_direccion_principal,
)
from usuarios.models import Usuario
from clientes.models import Cliente, Direccion

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
            
class DireccionTestCase(BaseTestCase):
    
    def test_listar_direcciones_devuelve_las_del_cliente(self):
        
        direccion1 = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=True,
        )
        
        direccion2 = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=True,
        )
        
        direcciones = listar_direcciones(self.cliente)
        
        self.assertEqual(
            set(direcciones),
            {direccion1, direccion2}
        )
        
    def test_listar_direcciones_no_devuelve_direcciones_de_otro_cliente(self):
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
        )
        
        otra_direccion = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Cra 20",
            ciudad="Bogotá",
            departamento="Cundinamarca",
        )
        
        direcciones = listar_direcciones(self.cliente)
        
        self.assertNotIn(
            otra_direccion,
            direcciones
        )
        
    def test_obtener_direccion_devuelve_la_direccion(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        resultado = obtener_direccion(
            direccion.pk,
            self.cliente
        )
        
        self.assertEqual(
            resultado,
            direccion
        )
        
    def test_obtener_direccion_de_otro_cliente_lanza_404(self):
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
        )
        
        direccion = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Cra 20",
            ciudad="Bogotá",
            departamento="Cundinamarca",
        )
        
        with self.assertRaises(Http404):
            obtener_direccion(
                direccion.pk,
                self.cliente,
            )
            
    def test_obtener_direccion_principal(self):
        
        principal = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=True,
        )
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        resultado = obtener_direccion_principal(
            self.cliente
        )
        
        self.assertEqual(
            resultado,
            principal
        )
        
    def test_obtener_direccion_principal_devuelve_none_si_no_existe(self):
        
        resultado = obtener_direccion_principal(
            self.cliente
        )
        
        self.assertIsNone(
            resultado
        )
