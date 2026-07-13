from django.db import models

class ImagenProducto(models.Model):
    
    producto = models.ForeignKey(
        "catalogo.Producto",
        on_delete=models.CASCADE,
        related_name="imagenes"
    )
    
    imagen = models.ImageField(upload_to="productos/")
    orden = models.PositiveSmallIntegerField(default=1)
    texto_alternativo = models.CharField(max_length=150, blank=True)
    
    class Meta:
        verbose_name = "Imagen del producto"
        verbose_name_plural = "Imágenes del producto"
        ordering = ["orden"]
        db_table = "imagenes_producto"
