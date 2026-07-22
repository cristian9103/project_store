from django.views.generic import ListView

from catalogo.models import Producto
from catalogo.selectors import buscar_productos

class ProductoListView(ListView):
    
    model = Producto
    
    template_name = "catalogo/lista_productos.html"
    
    context_object_name = "productos"
    
    paginate_by = 12
    
    def get_queryset(self):
        params = self.request.GET
        
        return buscar_productos(
            texto=params.get("buscar"),
            categoria=params.get("categoria"),
            marca=params.get("marca"),
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["buscar"] = self.request.GET.get("buscar", "")
        context["categoria"] = self.request.GET.get("categoria", "")
        context["marca"] = self.request.GET.get("marca", "")
        
        return context
