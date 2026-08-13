from pedidos.forms import CheckoutForm
from .base import BaseTestCase

class FormsTestCase(BaseTestCase):
    
    def test_checkout_form_requiere_direccion_id(self):
        form = CheckoutForm(data={})
        
        self.assertFalse(form.is_valid())
        
        self.assertIn(
            "direccion_id",
            form.errors,
        )
        
    def test_checkout_form_acepta_direccion_id_valido(self):
        form = CheckoutForm(
            data={
                "direccion_id": 5,
            }
        )
        
        self.assertTrue(form.is_valid())
        
        self.assertEqual(
            form.cleaned_data["direccion_id"],
            5,
        )
        
    def test_checkout_form_rechaza_direccion_id_no_numerico(self):
        form = CheckoutForm(
            data={
                "direccion_id": "abc",
            }
        )
        
        self.assertFalse(form.is_valid())
        
        self.assertIn(
            "direccion_id",
            form.errors,
        )
