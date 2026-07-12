from django.db import models

class Marca(models.Model):
    
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