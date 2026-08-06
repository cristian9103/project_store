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
        
        ordering = [
            "-es_principal",
            "-fecha_creacion",
        ]
        
        constraints = [
            models.UniqueConstraint(
                fields=["cliente"],
                condition=models.Q(
                    es_principal=True
                ),
                name="unique_direccion_principal_por_cliente",
            )
        ]
        
    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"
    
    @property
    def direccion_completa(self):
        return(
            f"{self.direccion}, "
            f"{self.ciudad}, "
            f"{self.departamento}"
        )
    