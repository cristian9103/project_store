from decimal import Decimal

from pedidos.models import DetallePedido
from pedidos.services import calcular_subtotal

from .base import BaseTestCase

class CalculosTestCase(BaseTestCase):
    
    def test_calcular_subtotal(self):
    
        # Arrange
        
        DetallePedido.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            precio_unitario=Decimal("20_000"),
            cantidad=2,
        )
        
        # Act
        
        subtotal = calcular_subtotal(self.pedido)
        
        # Assert
        
        self.assertEqual(
            subtotal,
            Decimal("40_000.00")
        )
