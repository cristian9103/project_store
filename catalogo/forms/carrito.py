from django import forms

class AgregarAlCarritoForm(forms.Form):
    
    cantidad = forms.IntegerField(
        label="Cantidad",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "min": 1,
            }
        ),
    )
    
    def __init__(self, *args, producto=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.producto = producto
        
    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]
        
        if self.producto and cantidad > self.producto.stock:
            raise forms.ValidationError(
                "No hay suficiente stock."
            )
            
        return cantidad
