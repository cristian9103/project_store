from django.urls import reverse

from clientes.models import Direccion, Cliente
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
        
    def test_listar_direcciones_no_muestra_las_de_otro_cliente(self):
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="456789123",
            telefono="30012345667",
        )
        
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
            cliente=otro_cliente,
            nombre="Casa de otro cliente",
            direccion="Carrera 80 # 50-60",
            ciudad="Bogotá",
            departamento="Cundinamarca",
            codigo_postal="110001",
            es_principal=True,
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse("clientes:lista_direcciones")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        direcciones = response.context["direcciones"]
        
        self.assertEqual(
            direcciones.count(),
            1,
        )
        
        self.assertEqual(
            direcciones.first().cliente,
            self.cliente,
        )
        
        self.assertEqual(
            direcciones.first().nombre,
            "Casa",
        )
        
    def test_obtener_direccion_muestra_direccion_del_cliente(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Carrera 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse(
                "clientes:detalle_direccion",
                kwargs={"pk": direccion.pk},
            )
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertEqual(
            response.context["direccion"],
            direccion,
        )
