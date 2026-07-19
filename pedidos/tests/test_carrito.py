from .base import BaseTestCase
from catalogo.models import Producto
from pedidos.services import (
    agregar_producto, 
    actualizar_cantidad, 
    ZERO, 
    eliminar_producto,
    vaciar_carrito
)

from pedidos.exceptions import (
    StockInsuficienteError, 
    CantidadInvalidaError,
    ProductoNoExisteEnPedidoError   
)

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
    def test_actualizar_cantidad_actualiza_detalle(self):
        
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
    
    def test_actualizar_cantidad_elimina_detalle_si_es_cero(self):
        
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
    
    def test_actualizar_cantidad_lanza_error_si_es_negativa(self):
        
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
    
    def test_actualizar_cantidad_lanza_error_si_producto_no_existe(self):
        
        # Act + Assert
        with self.assertRaises(ProductoNoExisteEnPedidoError):
            actualizar_cantidad(
                self.pedido,
                self.producto,
                nueva_cantidad=4
            )
    
    def test_actualizar_cantidad_lanza_error_si_supera_stock(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act + Assert
        with self.assertRaises(StockInsuficienteError):
            actualizar_cantidad(
                self.pedido,
                self.producto,
                nueva_cantidad=25
            )
            
        detalle = self.pedido.detalles_pedido.get()
        
        self.assertEqual(
            detalle.cantidad,
            2
        )
    
    #-----------------------------------------
    # eliminar_producto()
    #-----------------------------------------
    def test_eliminar_producto(self):
        
        # Arrange
        self.crear_detalle(cantidad=3)
        
        # Act
        resultado = eliminar_producto(
            self.pedido,
            self.producto
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
    
    #-----------------------------------------
    # vaciar_carrito()
    #-----------------------------------------
    def test_vaciar_carrito(self):
        
        # Arrange
        producto2 = Producto.objects.create(
            categoria=self.categoria,
            marca=self.marca,
            sku="CRE001",
            nombre="Crema Facial",
            descripcion="",
            precio_compra=Decimal("15_000.00"),
            precio_venta=Decimal("30_000.00"),
            stock=10,
        )
        
        self.crear_detalle(cantidad=2)
        
        self.crear_detalle(
            producto=producto2,
            cantidad=1
        )
        
        # Act
        pedido = vaciar_carrito(self.pedido)
        
        # Assert
        self.assertEqual(
            pedido.detalles_pedido.count(),
            0
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.subtotal,
            ZERO
        )
        
        self.assertEqual(
            pedido.total,
            ZERO
        )
        
    def test_vaciar_carrito_vacio(self):
        
        # Act
        pedido = vaciar_carrito(self.pedido)
        
        # Assert
        self.assertEqual(
            pedido.detalles_pedido.count(),
            0
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.subtotal,
            ZERO
        )
        
        self.assertEqual(
            pedido.total,
            ZERO
        )
    