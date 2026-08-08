from django import forms

from clientes.models import Direccion

class DireccionForm(forms.ModelForm):
    
    class Meta:
        model = Direccion
        fields = [
            "nombre",
            "direccion",
            "ciudad",
            "departamento",
            "codigo_postal",
            "es_principal",
        ]
