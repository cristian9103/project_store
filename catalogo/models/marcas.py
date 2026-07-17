from django.db import models
from core.models.base_model import BaseModel

class Marca(BaseModel):
    
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    logo = models.ImageField(upload_to="marcas/", blank=True, null=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["nombre"]
        db_table = "marcas"
        
    def __str__(self):
        return self.nombre