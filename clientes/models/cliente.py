from django.db import models
from django.conf import settings
from core.models.base_model import BaseModel

class Cliente(BaseModel):
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cliente"
    )
    
    documento = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Clente"
        verbose_name_plural = "Clientes"
        ordering = ["usuario__first_name"]
        db_table = "clientes"
        
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
    
    @property
    def esta_activo(self):
        return self.usuario.is_active