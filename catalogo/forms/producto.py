from django import forms

from catalogo.models import Categoria, Marca

class ProductoBusquedaForm(forms.Form):
    buscar = forms.CharField(
        required=False,
        max_length=100,
        label="Buscar",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Buscar productos...",
            }
        ),
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
    )
    
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        required=False,
        empty_label="Todas las marcas",
    )
    