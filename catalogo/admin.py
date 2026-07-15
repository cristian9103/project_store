from django.contrib import admin

from catalogo.models.categorias import Categoria
from catalogo.models.imagenes_producto import ImagenProducto
from catalogo.models.marcas import Marca
from catalogo.models.productos import Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "descripcion",
        "imagen",
        "activa",
    )
    
    search_fields = (
        "nombre",
        "descripcion",    
    )
    
    list_filter = ("nombre",)
    
    ordering = ("nombre",)
    
    
@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "imagen",
    )
    
    search_fields = ("producto__nombre",)
    
    list_filter = ("producto",)
    
    ordering = ("producto__nombre",)
    
    list_select_related = ("producto",)
    

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "descripcion",
        "activa",
    )
    
    search_fields = (
        "nombre",
        "descripcion",
    )
    
    list_filter = (
        "nombre",
        "descripcion",
    )
    
    ordering = ("nombre",)
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "categoria",
        "marca",
        "sku",
        "nombre",
        "descripcion",
        "precio_compra",
        "precio_venta",
        "stock",
        "activo",
        "fecha_creacion",
        "fecha_actualizacion",
    )
    
    search_fields = (
        "categoria__nombre",
        "marca__nombre",
        "sku",
        "nombre",
        "precio_compra",
        "precio_venta",
    )
    
    list_filter = (
        "categoria",
        "marca",
        "sku",
        "nombre",
        "precio_compra",
        "fecha_creacion",
        "fecha_actualizacion",
    )
    
    ordering = ("nombre",)
    
    list_select_related = ("categoria", "marca",)
