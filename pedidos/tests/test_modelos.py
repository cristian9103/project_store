from decimal import Decimal

from django.db import IntegrityError, transaction

from .base import BaseTestCase

class ModelosTestCase(BaseTestCase):
    
    def test_pedido_no_permite_total_negativo(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.pedido.total = Decimal("-1.00")
                self.pedido.save()
                
    def test_pedido_no_permite_subtotal_negativo(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.pedido.subtotal = Decimal("-1.00")
                self.pedido.save()
                
    def test_pedido_no_permite_costo_envio_negativo(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.pedido.costo_envio = Decimal("-1.00")
                self.pedido.save()
                
    def test_pedido_no_permite_descuento_negativo(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.pedido.descuento = Decimal("-1.00")
                self.pedido.save()
