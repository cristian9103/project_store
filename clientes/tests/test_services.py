from clientes.services import crear_direccion
from clientes.models import Direccion
from pedidos.tests import BaseTestCase

class DireccionTestCase(BaseTestCase):

    def test_crar_direccion(self):
        
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
        )
        
        self.assertEqual(
            direccion.cliente,
            self.cliente
        )
        
        self.assertEqual(
            direccion.nombre,
            "Casa"
        )
        
        self.assertTrue(
            Direccion.objects.filter(
                pk=direccion.pk
            ).exists()
        )
        
    def test_primera_direccion_se_convierte_en_principal(self):
        
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
        )
        
        self.assertTrue(
            direccion.es_principal
        )
        