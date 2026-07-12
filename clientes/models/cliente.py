from django.db import models
from django.conf import settings

class Cliente(models.Model):
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cliente"
    )
    
    documento = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Clente"
        verbose_name_plural = "Clientes"
        ordering = ["usuario__first_name"]
        db_table = "clientes"
        
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"