from django import forms
from django.contrib.auth.password_validation import validate_password

from usuarios.models import Usuario
from clientes.models import Cliente

class RegistroForm(forms.Form):
    
    email = forms.EmailField(
        label="Correo electrónico"
    )
    
    first_name = forms.CharField(
        label="Nombre",
        max_length=150
    )
    
    last_name = forms.CharField(
        label="Apellido",
        max_length=150
    )
    
    documento = forms.CharField(
        label="Documento",
        max_length=15
    )
    
    telefono = forms.CharField(
        label="Teléfono",
        max_length=20
    )
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )
    
    password_confirmacion = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Ya existe un usuario registrado con este correo."
            )
            
        return email
    
    def clean_documento(self):
        documento = self.cleaned_data["documento"]
        
        if Cliente.objects.filter(documento=documento).exists():
            raise forms.ValidationError(
                "Ya existe un cliente registrado con este documento."
            )
            
        return documento
    
    def clean_password(self):
        password = self.cleaned_data["password"]
        
        validate_password(password)
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get("password")
        password_confirmacion = cleaned_data.get("password_confirmacion")
        
        if (
            password
            and password_confirmacion
            and password != password_confirmacion
        ):
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )
            
        return cleaned_data
