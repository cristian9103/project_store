from .base import BaseTestCase
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
        pass
    
    def test_confirmar_pedido_actualiza_estado(self):
        pass
    
    def test_confirmar_pedido_descuenta_stock(self):
        pass
    
    def test_confirmar_pedido_actualiza_totales(self):
        pass
