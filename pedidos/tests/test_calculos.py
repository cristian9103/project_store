from decimal import Decimal

from pedidos.models import DetallePedido
from pedidos.services.calculos import calcular_subtotal
from catalogo.models import Producto

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
        
    def test_calcular_subtotal_con_un_producto(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        subtotal = calcular_subtotal(self.pedido)
        
        # Assert
        self.assertEqual(
            subtotal,
            Decimal("40_000.00")
        )
        
    def test_calcular_subtotal_con_varios_productos(self):
        
        # Arrange
        producto2 = Producto.objects.create(
            categoria=self.categoria,
            marca=self.marca,
            sku="CER001",
            nombre="Crema",
            precio_compra=Decimal("25_000"),
            precio_venta=Decimal("30_000"),
            stock=20,
        )
        
        # Act
        self.crear_detalle(cantidad=2)
        
        self.crear_detalle(
            producto=producto2,
            cantidad=1
        )
        
        subtotal = calcular_subtotal(self.pedido)
        
        # Assert
        self.assertEqual(
            subtotal,
            Decimal("70_000.00")
        )
        