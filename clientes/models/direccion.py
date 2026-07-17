from django.db import models
from core.models.base_model import BaseModel

class Direccion(BaseModel):
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        related_name="direcciones"
    )
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=70)
    departamento = models.CharField(max_length=70)
    codigo_postal = models.CharField(max_length=20, blank=True)
    es_principal = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        db_table = "direcciones"