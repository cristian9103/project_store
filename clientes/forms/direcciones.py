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
        widgets = {
            "nombre": forms.TelInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "direccion": forms.TelInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "ciudad": forms.TelInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "departamento": forms.TelInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "codigo_postal": forms.TelInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "es_principal": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
