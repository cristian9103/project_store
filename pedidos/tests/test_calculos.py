from decimal import Decimal

from pedidos.models import DetallePedido
from pedidos.services import (
    calcular_subtotal,
    actualizar_totales,
    ZERO,
) 
from catalogo.models import Producto

from .base import BaseTestCase


class CalculosTestCase(BaseTestCase):
    
    #-----------------------------------------
    # Calcular_subtotal()
    #-----------------------------------------
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
        
    def test_calcular_subtotal_sin_productos(self):
        
        # Act
        subtotal = calcular_subtotal(self.pedido)
        
        # Assert
        self.assertEqual(
            subtotal,
            ZERO
        )
        
    #-----------------------------------------
    # Calcular_total()
    #-----------------------------------------
    def test_calcular_total_sin_envio_ni_descuento(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        total = self.calcular_total_pedido()
        
        # Assert
        self.assertEqual(
            total,
            Decimal("40_000.00")
        )
    
    def test_calcular_total_con_envio(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        self.pedido.costo_envio = Decimal("8_000.00")
        
        # Act
        total = self.calcular_total_pedido()
        
        # Assert
        self.assertEqual(
            total,
            Decimal("48_000.00")
        )
    
    def test_calcular_total_con_descuento(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        self.pedido.descuento = Decimal("5_000.00")
        
        # Act
        total = self.calcular_total_pedido()
        
        # Assert
        self.assertEqual(
            total,
            Decimal("35_000.00")
        )
    
    def test_calcular_total_con_envio_y_descuento(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        self.pedido.costo_envio = Decimal("8_000.00")
        
        self.pedido.descuento = Decimal("3_000.00")
        
        # Act
        total = self.calcular_total_pedido()
        
        # Assert
        self.assertEqual(
            total,
            Decimal("45_000.00")
        )
        
    #-----------------------------------------
    # Actualizar_totales()
    #-----------------------------------------
    def test_actualizar_totales_actualiza_subtotal(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        actualizar_totales(self.pedido)
        
        self.pedido.refresh_from_db()
        
        # Assert
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("40_000.00")
        )
    
    def test_actualizar_totales_actualiza_total(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        self.pedido.costo_envio = Decimal("8_000.00")
        self.pedido.save(update_fields=["costo_envio"])
        
        # Act
        actualizar_totales(self.pedido)
        
        self.pedido.refresh_from_db()
        
        # Assert
        self.assertEqual(
            self.pedido.total,
            Decimal("48_000.00")
        )
        