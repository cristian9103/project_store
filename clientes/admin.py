from django.contrib import admin

from .models.cliente import Cliente
from .models.direccion import Direccion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    
    list_display = (
        "usuario",
        "documento",
        "telefono",
    )
    
    search_fields = (
        "documento",
        "usuario__email",
        "usuario__first_name",
        "usuario__last_name",
    )
    
@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "nombre",
        "direccion",
        "ciudad",
        "departamento",
        "codigo_postal",
        "es_principal",
    )
    
    search_fields = (
        "cliente__usuario__firtst_name",
        "ciudad",
        "departamento",
    )
    
    list_filter = (
        "ciudad",
        "departamento",
    )
    
    ordering = ("ciudad",)
    
    list_select_related = ("cliente",)
