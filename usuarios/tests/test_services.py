from django.contrib.auth import get_user_model
from django.db import IntegrityError

from usuarios.services import registrar_usuario
from .base import BaseTestCase

from clientes.models import Cliente

Usuario = get_user_model()

class RegistrarUsuarioTest(BaseTestCase):
    
    def test_registrar_usuario_crea_usuario(self):
        
        datos = self.datos_registro()
        
        registrar_usuario(**datos)
        
        self.assertTrue(
            Usuario.objects.filter(
                email=datos["email"]
            ).exists()
        )
        
    def test_registrar_usuario_crea_cliente(self):
        
        datos = self.datos_registro()
        
        registrar_usuario(**datos)
        
        self.assertTrue(
            Cliente.objects.filter(
                documento=datos["documento"]
            ).exists()
        )
        
    def test_registrar_usuario_asocia_cliente_con_usuario(self):
        
        datos = self.datos_registro()
        
        cliente = registrar_usuario(**datos)
        
        self.assertEqual(
            cliente.usuario.email,
            datos["email"]
        )
        
    def test_registrar_usuario_guarda_password_hasheado(self):
        
        datos = self.datos_registro()
        
        cliente = registrar_usuario(**datos)
        
        usuario = cliente.usuario
        
        self.assertNotEqual(
            usuario.password,
            datos["password"]
        )
        
        self.assertTrue(
            usuario.check_password(datos["password"])
        )
        
    def test_registrar_usuario_rollback_si_falla_cliente(self):
        
        datos = self.datos_registro()
        
        self.crear_cliente(
            documento=datos["documento"]
        )
        
        with self.assertRaises(IntegrityError):
            
            registrar_usuario(**datos)
            
        self.assertFalse(
            Usuario.objects.filter(
                email=datos["email"]
            ).exists()
        )
