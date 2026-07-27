from django import forms

class ActualizarCantidadForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=0,
        label="Cantidad",
    )
