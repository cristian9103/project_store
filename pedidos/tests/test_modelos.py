from decimal import Decimal

from django.db import IntegrityError, transaction

from .base import BaseTestCase
from pedidos.models import (
    DetallePedido,
    Pedido,
    EstadoPedido,
)
from pedidos.services import ZERO

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
        
    def test_pedido_no_permite_producto_duplicado(self):
        
        DetallePedido.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            precio_unitario=Decimal("20_000.00"),
            cantidad=1,
        )
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DetallePedido.objects.create(
                    pedido=self.pedido,
                    producto=self.producto,
                    precio_unitario=Decimal("20_000.00"),
                    cantidad=2
                )
                
    def test_mismo_producto_permitido_en_pedidos_diferentes(self):
        
        detalle_1 = DetallePedido.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            precio_unitario=Decimal("20_000.00"),
            cantidad=1,
        )
        
        otro_pedido = Pedido.objects.create(
            cliente=self.cliente,
            estado=EstadoPedido.PREPARACION,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        detalle_2 = DetallePedido.objects.create(
            pedido=otro_pedido,
            producto=self.producto,
            precio_unitario=Decimal("20_000.00"),
            cantidad=2,
        )
        
        self.assertEqual(
            detalle_1.producto,
            detalle_2.producto
        )
        
        self.assertNotEqual(
            detalle_1.pedido_id,
            detalle_2.pedido_id
        )
        
    def test_cliente_no_puede_tener_dos_pedidos_pendientes(self):
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Pedido.objects.create(
                    cliente=self.cliente,
                    estado=EstadoPedido.PENDIENTE,
                    subtotal=ZERO,
                    costo_envio=ZERO,
                    descuento=ZERO,
                    total=ZERO,
                )
                
    def test_cliente_puede_tener_varios_pedidos_no_pendientes(self):
        
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["estado"])
        
        segundo_pedido = Pedido.objects.create(
            cliente=self.cliente,
            estado=EstadoPedido.ENTREGADO,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        self.assertEqual(
            Pedido.objects.filter(
                cliente=self.cliente
            ).count(),
            2
        )
