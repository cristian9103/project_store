from django.urls import reverse

from clientes.models import Direccion
from clientes.tests import BaseTestCase

class DireccionViewTestCase(BaseTestCase):
    
    def test_crear_direccion_usuario_autenticado(self):
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("clientes:crear_direccion"),
            data={
                "nombre": "Casa",
                "direccion": "Carrera 10 # 20-30",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "050001",
                "es_principal": False,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        self.assertTrue(
            Direccion.objects.filter(
                cliente=self.cliente,
                nombre="Casa",
                direccion="Carrera 10 # 20-30",
            ).exists()
        )
