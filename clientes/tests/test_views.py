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
        
    def test_crear_direccion_usuario_no_autenticado_redirige_login(self):
        
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
        
        self.assertIn(
            "login",
            response.url,
        )
        
    def test_crear_direccion_formulario_invalido_no_crea_direccion(self):
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("clientes:crear_direccion"),
            data={
                "nombre": "",
                "direccion": "Carrera 10 # 20-30",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "",
                "es_principal": False,
            },
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertIn(
            "form",
            response.context
        )
        
        self.assertTrue(
            response.context["form"].errors
        )
        
        self.assertFalse(
            Direccion.objects.filter(
                cliente=self.cliente
            ).exists()
        )
        
    def test_crear_direccion_se_asocia_al_cliente_autenticado(self):
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("clientes:crear_direccion"),
            data={
                "nombre": "Trabajo",
                "direccion": "Carrera 50 # 10-20",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "050002",
                "es_principal": False,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        direccion = Direccion.objects.get(
            nombre="Trabajo"
        )
        
        self.assertEqual(
            direccion.cliente,
            self.cliente
        )
        
        self.assertEqual(
            direccion.cliente.usuario,
            self.usuario
        )
        
    def test_listar_direcciones_muestra_las_del_cliente(self):
        
        self.client.force_login(self.usuario)
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Carrera 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Trabajo",
            direccion="Carrera 50 # 10-20",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=False,
        )
        
        response = self.client.get(
            reverse("clientes:lista_direcciones")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertEqual(
            len(response.context["direcciones"]),
            2,
        )
