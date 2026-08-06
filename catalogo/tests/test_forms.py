from decimal import Decimal

from catalogo.forms import AgregarAlCarritoForm
from pedidos.tests.base import BaseTestCase

class AgregarAlCarritoFormTest(BaseTestCase):
    
    def test_cantidad_valida(self):
        
        form = AgregarAlCarritoForm(
            data={
                "cantidad": 2
            },
            producto=self.producto
        )
        
        self.assertTrue(
            form.is_valid()
        )
        
        self.assertEqual(
            form.cleaned_data["cantidad"],
            2
        )
        
    def test_cantidad_superior_stock_es_invalida(self):
        
        form = AgregarAlCarritoForm(
            data={
                "cantidad": 21
            },
            producto=self.producto
        )
        
        self.assertFalse(
            form.is_valid()
        )
        
        self.assertIn(
            "No hay suficiente stock.",
            form.errors["cantidad"]
        )
        
    def test_cantidad_cero_es_invalida(self):
        
        form = AgregarAlCarritoForm(
            data={
                "cantidad": 0
            },
            producto=self.producto
        )
        
        self.assertFalse(
            form.is_valid()
        )
        
        self.assertIn(
            "cantidad",
            form.errors
        )
        
    def test_cantidad_negativa_es_invalida(self):
        
        form = AgregarAlCarritoForm(
            data={
                "cantidad": -1
            },
            producto=self.producto
        )
        
        self.assertFalse(
            form.is_valid()
        )
        
        self.assertIn(
            "cantidad",
            form.errors
        )
        