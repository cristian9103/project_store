from django.urls import reverse

from .base import BaseTestCase

class LogoutViewTest(BaseTestCase):
        
    def test_logout_cierra_sesion(self):
        
        usuario = self.crear_usuario()
        
        self.client.force_login(usuario)
        
        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )
        
        url = reverse("usuarios:logout")
        
        response = self.client.post(url)
        
        self.assertRedirects(
            response,
            reverse("usuarios:login")
        )
        
        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )
        
    def test_usuario_puede_iniciar_sesion_despues_de_logout(self):
        
        password = "X7!mQ2#vR9@kL4"
        
        usuario = self.crear_usuario(
            email="logout@test.com",
            password=password
        )
        
        self.client.force_login(usuario)
        
        self.client.post(
            reverse("usuarios:logout")
        )
        
        response = self.client.post(
            reverse("usuarios:login"),
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
