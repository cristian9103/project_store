from django import forms

class CheckoutForm(forms.Form):
    direccion_id = forms.IntegerField(
        min_value=1,
    )
