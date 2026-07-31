from usuarios.forms import RegistroForm

from .base import BaseTestCase

class RegistroFormTest(BaseTestCase):
    
    def test_formulario_valido(self):
        
        datos = self.datos_registro(
            password_confirmacion="X7!mQ2#vR9@kL4"
        )
        
        form = RegistroForm(data=datos)
        
        self.assertTrue(form.is_valid())
        
    def test_email_duplicado(self):
        
        datos = self.datos_registro(
            password_confirmacion="X7!mQ2#vR9@kL4"
        )
        
        self.crear_usuario(
            email=datos["email"]
        )
        
        form = RegistroForm(data=datos)
        
        self.assertFalse(form.is_valid())
        
        self.assertIn(
            "email",
            form.errors
        )
        
    def test_documento_duplicado(self):
        
        datos = self.datos_registro()
        
        self.crear_cliente(
            documento=datos["documento"]
        )
        
        form = RegistroForm(data=datos)
        
        self.assertFalse(form.is_valid())
        
        self.assertIn(
            "documento",
            form.errors
        )
        
    def test_passwords_no_coinciden(self):
        
        datos = self.datos_registro(
            password_confirmacion="Y8@pL3#sW6!nR1"
        )
        
        form = RegistroForm(data=datos)
        
        self.assertFalse(form.is_valid())
        
        self.assertIn(
            "Las contraseñas no coinciden.",
            form.non_field_errors()
        )
        
    def test_password_invalida(self):
        
        datos = self.datos_registro(
            password="123",
            password_confirmacion="123",
        )
        
        form = RegistroForm(data=datos)
        
        self.assertFalse(form.is_valid())
        
        self.assertIn(
            "password",
            form.errors
        )
