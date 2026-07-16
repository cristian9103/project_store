from django.db import models
from django.core.validators import MinValueValidator

class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        "pedidos.Pedido",
        on_delete=models.CASCADE,
        related_name="detalles_pedido"
    )
    
    producto = models.ForeignKey(
        "catalogo.Producto",
        on_delete=models.PROTECT,
        related_name="detalles_pedido"
    )
    
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Detalle Pedido"
        verbose_name_plural = "Detalles Pedido"
        ordering = ["fecha_creacion"]
        db_table = "detalles_pedido"
        
        constraints = [
            models.UniqueConstraint(
                fields=["pedido", "producto"],
                name="unique_producto_por_pedido"
            )
        ]
        
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        
        super().save(*args, **kwargs)