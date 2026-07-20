from .base import BaseTestCase
from decimal import Decimal
from pedidos.services import crear_pedido, confirmar_pedido
from pedidos.models import Pedido, EstadoPedido
from pedidos.exceptions import (
    StockInsuficienteError,
    EstadoPedidoInvalidoError,
    PedidoVacioError
)

class PedidosTestCase(BaseTestCase):
    
    #-----------------------------------------
    # crear_pedido()
    #-----------------------------------------
    def test_crear_pedido_retorna_pedido_existente(self):
        
        # Act
        pedido = crear_pedido(self.cliente)
        
        # Assert
        self.assertEqual(
            pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            Pedido.objects.filter(
                cliente=self.cliente,
                estado=EstadoPedido.PENDIENTE
            ).count(),
            1
        )
    
    def test_crear_pedido_crea_un_nuevo_pedido(self):
        
        # Arrange
        self.pedido.estado = EstadoPedido.ENTREGADO
        
        self.pedido.save(update_fields=["estado"])
        
        # Act
        pedido = crear_pedido(self.cliente)
        
        # Assert
        self.assertNotEqual(
            pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PENDIENTE
        )
    
    #-----------------------------------------
    # confirmar_pedido()
    #-----------------------------------------
    def test_confirmar_pedido_lanza_error_si_esta_vacio(self):
        
        # Act + Assert
        with self.assertRaises(PedidoVacioError):
            confirmar_pedido(self.pedido)
    
    def test_confirmar_pedido_lanza_error_si_no_hay_stock(self):
        
        # Arrange
        self.crear_detalle(cantidad=25)
        
        # Act + Assert
        with self.assertRaises(StockInsuficienteError):
            confirmar_pedido(self.pedido)
            
        self.producto.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            20
        )
    
    def test_confirmar_pedido_lanza_error_si_estado_no_es_pendiente(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        self.pedido.estado = EstadoPedido.CANCELADO
        
        self.pedido.save(update_fields=["estado"])
        
        # Act
        with self.assertRaises(EstadoPedidoInvalidoError):
            confirmar_pedido(self.pedido)
            
        # Assert
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.CANCELADO
        )
    
    def test_confirmar_pedido_actualiza_estado(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        pedido = confirmar_pedido(self.pedido)
        
        # Assert
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PREPARACION
        )
    
    def test_confirmar_pedido_descuenta_stock(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        confirmar_pedido(self.pedido)
        
        # Assert
        self.producto.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            18
        )
    
    def test_confirmar_pedido_actualiza_totales(self):
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        self.pedido.costo_envio = Decimal("8_000.00")
        self.pedido.save(update_fields=["costo_envio"])
        
        # Act
        pedido = confirmar_pedido(self.pedido)
        
        # Assert
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.subtotal,
            Decimal("40_000.00")
        )
        
        self.assertEqual(
            pedido.total,
            Decimal("48_000.00")
        )
