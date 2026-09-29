from django.urls import reverse

from decimal import Decimal

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
        
    def test_detalle_producto_agregar_al_carrito_actualiza_totales(self):
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
        
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("40_000"),
        )
        
        self.assertEqual(
            self.pedido.total,
            Decimal("40_000"),
        )
        
    def test_detalle_producto_agregar_al_carrito_producto_existente_suma_cantidad(self):
        self.client.force_login(self.usuario)
        
        self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={"pk": self.producto.pk},
            ),
            data={
                "cantidad": 2,
            },
        )
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={"pk": self.producto.pk},
            ),
            data={
                "cantidad": 3,
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
            5,
        )
        
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("100_000"),
        )
        
        self.assertEqual(
            self.pedido.total,
            Decimal("100_000"),
        )
        
    def test_detalle_producto_agregar_al_carrito_requiere_login(self):
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
        
        self.assertIn(
            "/usuarios/login/",
            response.url,
        )
        
        self.assertFalse(
            self.pedido.detalles_pedido.exists()
        )
        
    def test_detalle_producto_agregar_al_carrito_cantidad_invalida(self):
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={"pk": self.producto.pk},
            ),
            data={
                "cantidad": 0,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        self.assertRedirects(
            response,
            reverse(
                "catalogo:detalle_producto",
                kwargs={"pk": self.producto.pk},
            ),
        )
        
        self.assertFalse(
            self.pedido.detalles_pedido.exists()
        )
        
    def test_detalle_producto_agregar_al_carrito_stock_insuficiente(self):
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={"pk": self.producto.pk},
            ),
            data={
                "cantidad": 21,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        self.assertRedirects(
            response,
            reverse(
                "catalogo:detalle_producto",
                kwargs={"pk": self.producto.pk},
            ),
        )
        
        self.assertFalse(
            self.pedido.detalles_pedido.exists()
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.subtotal,
            Decimal("0"),
        )
        
        self.assertEqual(
            self.pedido.total,
            Decimal("0"),
        )

class ProductoListViewTest(BaseTestCase):
    
    def test_catalogo_muestra_producto_sin_stock(self):
        self.producto.stock = 0
        self.producto.save(update_fields=["stock"])
        
        response = self.client.get(
            reverse("catalogo:lista_productos")
        )
        
        self.assertContains(
            response,
            self.producto.nombre
        )
        
    def test_busqueda_muestra_producto_sin_stock(self):
        self.producto.stock = 0
        self.producto.save(update_fields=["stock"])
        
        response = self.client.get(
            reverse("catalogo:lista_productos"),
            {"buscar": self.producto.nombre},
        )
        
        self.assertContains(
            response,
            self.producto.nombre,
        )
        