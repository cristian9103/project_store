from pedidos.services import validar_stock
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
        
        with self.assertRaises(StockInsuficienteError):
            
            validar_stock(
                self.producto,
                25
            )
    