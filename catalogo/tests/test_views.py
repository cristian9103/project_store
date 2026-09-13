from django.urls import reverse

from core.tests import BaseTestCase

class ProductoDetailViewTest(BaseTestCase):
    
    def test_detalle_producto_muestra_boton_agregar_al_carrito(self):
        response = self.client.get(
            reverse(
                "catalogo:detalle_producto",
                kwargs={"pk": self.producto.pk},
            )
        )
        
        self.assertContains(
            response,
            "Agregar al carrito",
        )
