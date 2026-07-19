from .base import BaseTestCase
from pedidos.services import agregar_producto, actualizar_cantidad, ZERO
from pedidos.exceptions import StockInsuficienteError, CantidadInvalidaError
from decimal import Decimal

class CarritoTestCase(BaseTestCase):
    
    #-----------------------------------------
    # agregar_producto()
    #-----------------------------------------
    def test_agregar_producto_nuevo(self):
        
        # Act
        detalle = agregar_producto(
            self.pedido,
            self.producto,
            cantidad=2
        )
        
        # Assert
        self.assertEqual(
            self.pedido.detalles_pedido.count(),
            1
        )
        
        self.assertEqual(
            detalle.cantidad,
            2
        )
        
        self.assertEqual(
            detalle.precio_unitario,
            self.producto.precio_venta
        )
        
        self.assertEqual(
            detalle.producto,
            self.producto
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("40_000.00")
        )
        
        self.assertEqual(
            self.pedido.total,
            Decimal("40_000.00")
        )
    
    def test_agregar_producto_existente(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        detalle = agregar_producto(
            self.pedido,
            self.producto,
            cantidad=3
        )
        
        # Assert
        self.assertEqual(
            self.pedido.detalles_pedido.count(),
            1
        )
        
        self.assertEqual(
            detalle.cantidad,
            5
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("100_000.00")
        )
    
    def test_agregar_producto_sin_stock(self):
        
        # Act
        with self.assertRaises(StockInsuficienteError):
            agregar_producto(
                self.pedido,
                self.producto,
                cantidad=25
            )
            
        self.assertEqual(
            self.pedido.detalles_pedido.count(),
            0
        )
    
    #-----------------------------------------
    # actualizar_cantidad()
    #-----------------------------------------
    def test_actualizar_cantidad(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        detalle = actualizar_cantidad(
            self.pedido,
            self.producto,
            nueva_cantidad=5
        )
        
        # Assert
        self.assertEqual(
            detalle.cantidad,
            5
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("100_000.00")
        )
        
        self.assertEqual(
            self.pedido.total,
            Decimal("100_000.00")
        )
    
    def test_actualizar_cantidad_a_cero(self):
        
        # Arrange
        self.crear_detalle(cantidad=3)
        
        # Act
        resultado = actualizar_cantidad(
            self.pedido,
            self.producto,
            nueva_cantidad=0
        )
        
        # Assert
        self.assertIsNone(resultado)
        
        self.assertEqual(
            self.pedido.detalles_pedido.count(),
            0
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.subtotal,
            ZERO
        )
        
        self.assertEqual(
            self.pedido.total,
            ZERO
        )
    
    def test_actualizar_cantidad_negativa(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act + Assert
        with self.assertRaises(CantidadInvalidaError):
            actualizar_cantidad(
                self.pedido,
                self.producto,
                nueva_cantidad=-3
            )
            
        detalle = self.pedido.detalles_pedido.get()
        
        self.assertEqual(
            detalle.cantidad,
            2
        )
    
    def test_actualizar_cantidad_producto_inexistente():
        pass
    
    def test_actualizar_cantidad_supera_stock(self):
        pass
    
    #-----------------------------------------
    # eliminar_producto()
    #-----------------------------------------
    def test_eliminar_producto(self):
        pass
    
    #-----------------------------------------
    # vaciar_carrito()
    #-----------------------------------------
    def test_vaciar_carrito(self):
        pass
    