from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["username"].label = "Correo electrónico"
        
        self.fields["username"].widget.attrs.update({
            "placeholder": "correo@ejemplo.com",
            "autocomplete": "email",
        })
        
        self.fields["password"].widget.attrs.update({
            "placeholder": "Contraseña",
            "autocomplete": "current-password",
        })
