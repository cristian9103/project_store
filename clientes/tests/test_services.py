from clientes.services import crear_direccion, establecer_principal
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
        
    def test_establecer_principal_actualiza_la_direccion_principal(self):
        
        direccion1 = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        direccion2 = crear_direccion(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        establecer_principal(direccion2)
        
        direccion1.refresh_from_db()
        direccion2.refresh_from_db()
        
        self.assertFalse(
            direccion1.es_principal
        )
        
        self.assertTrue(
            direccion2.es_principal
        )
        
    def test_establecer_principal_deja_una_sola_direccion_principal(self):
        
        crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        direccion2 = crear_direccion(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        establecer_principal(direccion2)
        
        self.assertEqual(
            Direccion.objects.filter(
                cliente=self.cliente,
                es_principal=True,
            ).count(),
            1,
        )
        
    def test_actualizar_direccion(self):
        
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        actualizar_direccion(
            direccion,
            nombre="Oficina",
            direccion_texto="Cra 50",
            ciudad="Bogotá",
            departamento="Cundinamarca",
            codigo_postal="110111",
            es_principal=True,
        )
        
        direccion.refresh_from_db()
        
        self.assertEqual(
            direccion.nombre,
            "Oficina"
        )
        
        self.assertEqual(
            direccion.ciudad,
            "Bogotá"
        )
        
        self.assertTrue(
            direccion.es_principal
        )
        