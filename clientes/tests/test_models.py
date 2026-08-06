from django.db import IntegrityError

from .base import BaseTestCase
from clientes.models import Cliente, Direccion
from usuarios.models import Usuario

class ClienteModelTest(BaseTestCase):
    
    def test_str_devuelve_nombre_completo(self):
        
        self.assertEqual(
            str(self.cliente),
            "Cristian Ramirez"
        )
        
    def test_esta_activo_devuelve_true_si_usuario_activo(self):
        
        self.assertTrue(
            self.usuario.is_active
        )
        
        self.assertTrue(
            self.cliente.esta_activo
        )
        
    def test_esta_activo_devuelve_false_si_usuario_inactivo(self):
        
        self.usuario.is_active = False
        self.usuario.save()
        
        self.cliente.refresh_from_db()
        
        self.assertFalse(
            self.cliente.esta_activo
        )
        
    def test_documento_debe_ser_unico(self):
        
        with self.assertRaises(IntegrityError):
            
            Cliente.objects.create(
                usuario=Usuario.objects.create_user(
                    email="otro@test.com",
                    password="123456789",
                    first_name="Otro",
                    last_name="Cliente",
                ),
                documento=self.cliente.documento,
                telefono="3111234567",
            )
            
    def test_usuario_no_puede_tener_dos_clientes(self):
        
        with self.assertRaises(IntegrityError):
            
            Cliente.objects.create(
                usuario=self.usuario,
                documento="987654321",
                telefono="3111234567",
            )
            
    def test_usuario_puede_acceder_a_su_cliente(self):
        
        self.assertEqual(
            self.usuario.cliente,
            self.cliente
        )
        
    def test_eliminar_usuario_elimina_cliente(self):
        
        cliente_id = self.cliente.pk
        
        self.usuario.delete()
        
        self.assertFalse(
            Cliente.objects.filter(
                pk=cliente_id
            ).exists()
        )
        
class DireccionModelTest(BaseTestCase):
    
    def test_crear_direccion_correctamente(self):
        
        direccion = self.crear_direccion()
        
        self.assertEqual(
            direccion.cliente,
            self.cliente
        )
        
        self.assertEqual(
            direccion.nombre,
            "Casa"
        )
        
        self.assertEqual(
            direccion.direccion,
            "Carrera 10 # 20-30"
        )
        
        self.assertEqual(
            direccion.ciudad,
            "Medellín"
        )
        
        self.assertEqual(
            direccion.departamento,
            "Antioquia"
        )
        
    def test_cliente_puede_tener_varias_direcciones(self):
        
        casa = self.crear_direccion(
            nombre="Casa"
        )
        
        trabajo = self.crear_direccion(
            nombre="Trabajo",
            direccion="Calle 50 # 40-20"
        )
        
        self.assertEqual(
            self.cliente.direcciones.count(),
            2
        )
        
        self.assertIn(
            casa,
            self.cliente.direcciones.all()
        )
        
        self.assertIn(
            trabajo,
            self.cliente.direcciones.all()
        )
        
    def test_direccion_no_es_principal_por_defecto(self):
        
        direccion = self.crear_direccion()
        
        self.assertFalse(
            direccion.es_principal
        )
        
    def test_direccion_puede_ser_principal(self):
        
        direccion = self.crear_direccion(
            es_principal=True
        )
        
        self.assertTrue(
            direccion.es_principal
        )
        
    def test_cliente_accede_a_sus_direcciones(self):
        
        direccion = self.crear_direccion()
        
        self.assertEqual(
            self.cliente.direcciones.first(),
            direccion
        )
        
    def test_eliminar_cliente_elimina_sus_direcciones(self):
        
        direccion = self.crear_direccion()
        
        direccion_id = direccion.pk
        
        self.cliente.delete()
        
        self.assertFalse(
            Direccion.objects.filter(
                pk=direccion_id
            ).exists()
        )
        
    def test_crear_direccion(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001"
        )
        
        self.assertEqual(
            direccion.cliente,
            self.cliente
        )
        
        self.assertFalse(
            direccion.es_principal
        )
        
    def test_direccion_completa(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001"
        )
        
        self.assertEqual(
            direccion.direccion_completa,
            "Cra 10 #20-30, Medellín, Antioquia"
        )
        
    def test_str(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001"
        )
        
        self.assertEqual(
            str(direccion),
            "Casa - Medellín"
        )
        
    def test_cliente_no_puede_tener_dos_direcciones_principales(self):
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=True,
        )
        
        with self.assertRaises(
            IntegrityError
        ):
            Direccion.objects.create(
                cliente=self.cliente,
                nombre="Oficina",
                direccion="Cra 50 #40-20",
                ciudad="Medellín",
                departamento="Antioquia",
                es_principal=True,
            )
            
    def test_cliente_puede_tener_varias_direcciones_secundarias(self):
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        Direccion.objects.create(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
        )
        
        self.assertEqual(
            self.cliente.direcciones.count(),
            2
        )
        
    def test_ordering_muestra_principal_primero(self):
        
        secundaria = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=False,
        )
        
        principal = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Cra 50",
            ciudad="Medellín",
            departamento="Antioquia",
            es_principal=True,
        )
        
        direcciones = list(
            Direccion.objects.all()
        )
        
        self.assertEqual(
            direcciones[0],
            principal
        )
        
        self.assertEqual(
            direcciones[1],
            secundaria
        )
        