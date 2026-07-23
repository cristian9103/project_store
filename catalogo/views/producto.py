from django.views.generic import ListView, DetailView

from catalogo.models import Producto
from catalogo.selectors import buscar_productos
from catalogo.forms import ProductoBusquedaForm

class ProductoListView(ListView):
    
    model = Producto
    
    template_name = "catalogo/lista_productos.html"
    
    context_object_name = "productos"
    
    paginate_by = 12
    
    def get_queryset(self):
        self.form = ProductoBusquedaForm(self.request.GET)
        
        if self.form.is_valid():
            return buscar_productos(
                texto=self.form.cleaned_data["buscar"],
                categoria=self.form.cleaned_data["categoria"],
                marca=self.form.cleaned_data["marca"],
            )
            
        return Producto.objects.disponibles()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["form"] = self.form
        
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        
        context["query_params"] = query_params.urlencode()
        
        return context
    
class ProductoDetailView(DetailView):
    model = Producto
    
    template_name = "catalogo/detalle_producto.html"
    
    context_object_name = "producto"
    
    def get_queryset(self):
        return (
            Producto.objects.disponibles()
            .select_related(
                "categoria",
                "marca",
            )
            .prefech_related(
                "imagenes",
            )
        )
