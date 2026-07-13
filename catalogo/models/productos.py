from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    
    categoria = models.ForeignKey(
        "catalogo.Categoria",
        on_delete=models.PROTECT,
        related_name="productos"
    )
    
    marca = models.ForeignKey(
        "catalogo.Marca",
        on_delete=models.PROTECT,
        related_name="productos"
    )
    
    sku = models.CharField(
        max_length=30, 
        unique=True,
        help_text="Código interno del producto."
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    precio_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    stock = models.PositiveIntegerField(
        help_text="Cantidad disponible para la venta."
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-fecha_creacion"]
        db_table = "productos"
        
    def __str__(self):
        return self.nombre
    
    @property
    def disponible(self):
        return self.activo and self.stock > 0
    
    @property
    def utilidad(self):
        return self.precio_venta - self.precio_compra