from django.views.generic import ListView

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
        
        return context
