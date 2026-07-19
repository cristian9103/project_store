from pedidos.services import validar_stock, descontar_stock
from pedidos.exceptions import StockInsuficienteError
from .base import BaseTestCase

class StockTestCase(BaseTestCase):
    
    #-----------------------------------------
    # validar_stock()
    #-----------------------------------------
    def test_validar_stock_suficiente(self):
        
        validar_stock(
            self.producto,
            5
        )
        
    def test_validar_stock_insuficiente(self):
        
        # Act
        with self.assertRaises(StockInsuficienteError) as error:
            
            validar_stock(
                self.producto,
                25
            )
            
        # Assert
        self.assertEqual(
            str(error.exception),
            "No hay stock suficiente."
        )
    #-----------------------------------------
    # descontar_stock()
    #-----------------------------------------
    def test_descontar_stock_reduce_existencias(self):
        
        # Act
        descontar_stock(
            self.producto,
            5
        )
        
        self.producto.refresh_from_db()
        
        # Assert
        self.assertEqual(
            self.producto.stock,
            15
        )
        
    def test_descontar_stock_sin_stock(self):
        
        # Act
        with self.assertRaises(StockInsuficienteError):
            descontar_stock(
                self.producto,
                50
            )
            
        self.producto.refresh_from_db()
        
        # Assert
        self.assertEqual(
            self.producto.stock,
            20
        )
        