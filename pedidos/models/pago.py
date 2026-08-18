from django.db import models

from core.models import BaseModel

class EstadoPago(models.TextChoices):
    PENDIENTE = "PE", "Pendiente"
    APROBADO = "AP", "Aprobado"
    RECHAZADO = "RE", "Rechazado"
    
class Pago(BaseModel):
    pedido = models.ForeignKey(
        "pedidos.Pedido",
        on_delete=models.PROTECT,
        related_name="pagos",
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
        
        constraints = [
            models.UniqueConstraint(
                fields=["pedido"],
                condition=models.Q(
                    estado=EstadoPago.PENDIENTE
                ),
                name="unique_pago_pendiente_por_pedido",
            ),
        ]
        
    def __str__(self):
        return f"Pago del pedido #{self.pedido_id}"
