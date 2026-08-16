from django.db import models

from core.models import BaseModel

class EstadoPago(models.TextChoices):
    PENDIENTE = "PE", "Pendiente"
    APROBADO = "AP", "Aprobado"
    RECHAZADO = "RE", "Rechazado"
    
class Pago(BaseModel):
    pedido = models.OneToOneField(
        "pedidos.Pedido",
        on_delete=models.PROTECT,
        related_name="pago",
    )
    
    estado = models.CharField(
        max_length=2,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
    )
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = "pagos"
        
    def __str__(self):
        return f"Pago del pedido #{self.pedido_id}"
