from decimal import Decimal

from django.db import IntegrityError, transaction

from .base import BaseTestCase
from pedidos.models import DetallePedido

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
                
    def test_detalle_no_permite_cantidad_cero(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DetallePedido.objects.create(
                    pedido=self.pedido,
                    producto=self.producto,
                    precio_unitario=Decimal("20_000.00"),
                    cantidad=0,
                )
                
    def test_detalle_no_permite_precio_unitario_negativo(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DetallePedido.objects.create(
                    pedido=self.pedido,
                    producto=self.producto,
                    precio_unitario=Decimal("-1.00"),
                    cantidad=1
                )
                
    def test_detalle_calcula_subtotal_automaticamente(self):
      
        detalle = DetallePedido.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            precio_unitario=Decimal("20_000.00"),
            cantidad=3,
        )
        
        self.assertEqual(
            detalle.subtotal,
            Decimal("60_000.00")
        )
