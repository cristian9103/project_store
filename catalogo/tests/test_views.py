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
        
    def test_detalle_producto_formulario_agregar_al_carrito(self):
        response = self.client.get(
            reverse(
                "catalogo:detalle_producto",
                kwargs={"pk": self.producto.pk},
            )
        )
        
        self.assertContains(
            response,
            '<form',
            html=False,
        )
        
        self.assertContains(
            response,
            'method="post"',
            html=False,
        )
        
        self.assertContains(
            response,
            reverse(
                "pedidos:agregar_producto",
                kwargs={"pk": self.producto.pk},
            ),
            html=False,
        )
        
    def test_detalle_producto_agregar_al_carrito(self):
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={"pk": self.producto.pk},
            ),
            data={
                "cantidad": 2,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        self.pedido.refresh_from_db()
        
        detalle = self.pedido.detalles_pedido.get(
            producto=self.producto
        )
        
        self.assertEqual(
            detalle.cantidad,
            2,
        )
