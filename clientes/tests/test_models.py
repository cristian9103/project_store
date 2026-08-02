from django.db import IntegrityError

from .base import BaseTestCase
from clientes.models import Cliente
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
