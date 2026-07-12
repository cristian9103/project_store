from django.db import models

class Categoria(models.Model):
    
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="categorias/", blank=True, null=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]
        db_table = "categorias"
        
    def __str__(self):
        return self.nombre