from django import forms

class CheckoutForm(forms.Form):
    direccion_id = forms.IntegerField(
        min_value=1,
        required=True,
        error_messages={
            "required": "Selecciona una dirección de envío."
        },
    )
