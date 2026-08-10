from clientes.services import (
    crear_direccion, 
    establecer_principal,
    actualizar_direccion,
    eliminar_direccion,
)
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
        
    def test_actualizar_direccion_no_cambia_principal_si_es_principal_false(self):
        
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
        
        actualizar_direccion(
            direccion2,
            nombre="Oficina nueva",
            direccion_texto="Cra 55",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="",
            es_principal=False,
        )
        
        direccion1.refresh_from_db()
        direccion2.refresh_from_db()
        
        self.assertTrue(
            direccion1.es_principal
        )
        
        self.assertFalse(
            direccion2.es_principal
        )
        
    def test_actualizar_codigo_postal(self):
        
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        actualizar_direccion(
            direccion,
            nombre="casa",
            direccion_texto="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=False,
        )
        
        direccion.refresh_from_db()
        
        self.assertEqual(
            direccion.codigo_postal,
            "050001"
        )
        
    def test_eliminar_direccion_secundaria(self):
        
        principal = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        secundaria = crear_direccion(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        eliminar_direccion(secundaria)
        
        self.assertFalse(
            Direccion.objects.filter(
                pk=secundaria.pk
            ).exists()
        )
        
        principal.refresh_from_db()
        
        self.assertTrue(
            principal.es_principal
        )
        
    def test_eliminar_principal_asigna_otra_principal(self):
        
        principal = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        secundaria = crear_direccion(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        eliminar_direccion(principal)
        
        secundaria.refresh_from_db()
        
        self.assertTrue(
            secundaria.es_principal
        )
        
        self.assertFalse(
            Direccion.objects.filter(
                pk=principal.pk
            ).exists()
        )
        
    def test_eliminar_unica_direccion(self):
        
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        eliminar_direccion(direccion)
        
        self.assertFalse(
            Direccion.objects.filter(
                pk=direccion.pk
            ).exists()
        )
        
    def test_actualizar_direccion_puede_quitar_principal(self):
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=True,
        )
        
        actualizar_direccion(
            direccion,
            nombre="Casa",
            direccion_texto="Calle 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=False,
        )
        
        direccion.refresh_from_db()
        
        self.assertFalse(
            direccion.es_principal
        )
        
    def test_actualizar_direccion_puede_establecer_principal(self):
        direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=False,
        )
        
        actualizar_direccion(
            direccion,
            nombre="Casa",
            direccion_texto="Calle 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        direccion.refresh_from_db()
        
        self.assertTrue(
            direccion.es_principal
        )
        
    def test_actualizar_direccion_nueva_principal_desactiva_la_anterior(self):
        direccion_principal = crear_direccion(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        otra_direccion = crear_direccion(
            cliente=self.cliente,
            nombre="Trabajo",
            direccion="Carrera 50",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=False,
        )
        
        actualizar_direccion(
            otra_direccion,
            nombre="Trabajo",
            direccion_texto="Carrera 50",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=True,
        )
        
        direccion_principal.refresh_from_db()
        otra_direccion.refresh_from_db()
        
        self.assertFalse(
            direccion_principal.es_principal
        )
        
        self.assertTrue(
            otra_direccion.es_principal
        )
        