from django.contrib.auth import get_user_model
from django.urls import reverse

from .base import BaseTestCase

Usuario = get_user_model()

class LoginViewTest(BaseTestCase):
    
    def test_get_muestra_formulario(self):
        
        url = reverse("usuarios:login")
        
        response = self.client.get(url)
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertTemplateUsed(
            response,
            "usuarios/login.html"
        )
        
        self.assertIn(
            "form",
            response.context
        )
        
    def test_login_correcto(self):
        
        password = "X7!mQ2#vR9@kL4"
        
        usuario = self.crear_usuario(
            email="login@test.com",
            password=password
        )
        
        url = reverse("usuarios:login")
        
        response = self.client.post(
            url,
            data={
                "username": usuario.email,
                "password": password,
            }
        )
        
        self.assertEqual(
            response.status_code,
            302
        )
        
        self.assertEqual(
            str(usuario.pk),
            self.client.session["_auth_user_id"]
        )
        
    def test_login_con_password_incorrecta(self):
        
        self.crear_usuario(
            email="login@test.com",
            password="X7!mQ2#vR9@kL4"
        )
        
        url = reverse("usuarios:login")
        
        response = self.client.post(
            url,
            data={
                "username": "login@test.com",
                "password": "PasswordIncorrecta123!",
            }
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )
        
    def test_login_usuario_inexistente(self):
        
        url = reverse("usuarios:login")
        
        response = self.client.post(
            url,
            data={
                "username": "noexiste@test.com",
                "password": "X7!mQ2#vR9@kL4",
            }
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )
        
    def test_login_usuario_inactivo(self):
        
        password = "X7!mQ2#vR9@kL4"
        
        usuario = self.crear_usuario(
            email="inactivo@test.com",
            password=password
        )
        
        usuario.is_active = False
        usuario.save(update_fields=["is_active"])
        
        url = reverse("usuarios:login")
        
        response = self.client.post(
            url,
            data={
                "username": usuario.email,
                "password": password,
            }
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )
