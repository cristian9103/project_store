from django.db import models

class ProductoQuerySet(models.QuerySet):
    
    def activos(self):
        return self.filter(activo=True)
    
    def con_stock(self):
        return self.filter(stock__gt=0)
    
    def disponibles(self):
        return self.activos().con_stock()
    