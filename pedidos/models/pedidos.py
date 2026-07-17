from django.db import models
from django.core.validators import MinValueValidator
from core.models.base_model import BaseModel

class EstadoPedido(models.TextChoices):
    PENDIENTE = "PE", "Pendiente"
    PAGADO = "PA", "Pagado"
    PREPARACION = "PR", "En preparación"
    ENVIADO = "EN", "Enviado"
    ENTREGADO = "ET", "Entregado"
    CANCELADO = "CA", "Cancelado"

class Pedido(BaseModel):
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="pedidos"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    
    estado = models.CharField(
        max_length=2,
        choices=EstadoPedido.choices,
        default=EstadoPedido.PENDIENTE
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    costo_envio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-fecha"]
        db_table = "pedidos"
        
    def __str__(self):
        return f"Pedido # {self.pk} - {self.cliente}"
