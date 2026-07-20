from django.views.generic import ListView

from catalogo.models import Producto

class ProductoListView(ListView):
    
    model = Producto
    
    queryset = Producto.objects.disponibles()
    
    template_name = "catalogo/lista_productos.html"
    
    context_object_name = "productos"
    
    paginate_by = 12
