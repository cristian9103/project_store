from django.contrib.auth.views import LoginView

from usuarios.forms import LoginForm

class UsuarioLoginView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
