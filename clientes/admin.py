from django.contrib import admin

from .models.cliente import Cliente

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
