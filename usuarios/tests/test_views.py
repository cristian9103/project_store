from django.contrib.auth import get_user_model
from django.urls import reverse

from usuarios.tests import BaseTestCase
from clientes.models import Cliente

Usuario = get_user_model()

class RegistroViewTest(BaseTestCase):
    
    def test_get_muestra_formulario(self):
        
        url = reverse("usuarios:registro")
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(
            response,
            "usuarios/registro.html"
        )
        
        self.assertIn(
            "form",
            response.context
        )
        
    def test_post_registro_valido_crea_usuario_y_cliente(self):
        
        datos = self.datos_registro(
            password_confirmacion="X7!mQ2#vR9@kL4"
        )
        
        url = reverse("usuarios:registro")
        
        response = self.client.post(
            url,
            data=datos
        )
        
        self.assertEqual(
            response.status_code,
            302
        )
        
        self.assertTrue(
            Usuario.objects.filter(
                email=datos["email"]
            ).exists()
        )
        
        self.assertTrue(
            Cliente.objects.filter(
                documento=datos["documento"]
            ).exists()
        )
        
    def test_post_registro_valido_inicia_sesion(self):
        
        datos = self.datos_registro(
            password_confirmacion="X7!mQ2#vR9@kL4"
        )
        
        url = reverse("usuarios:registro")
        
        self.client.post(
            url,
            data=datos
        )
        
        usuario = Usuario.objects.get(
            email=datos["email"]
        )
        
        self.assertEqual(
            str(usuario.pk),
            self.client.session["_auth_user_id"]
        )
        
    def test_post_registro_invalido_no_crea_usuario(self):
        
        datos = self.datos_registro()
        
        self.crear_usuario(
            email=datos["email"]
        )
        
        url = reverse("usuarios:registro")
        
        response = self.client.post(
            url,
            data=datos
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertFormError(
            response.context["form"],
            "email",
            "Ya existe un usuario registrado con este correo."
        )
