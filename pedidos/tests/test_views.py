from django.urls import reverse
from django.contrib.messages import get_messages

from .base import BaseTestCase
from clientes.models import Cliente
from usuarios.models import Usuario
from pedidos.models import Pedido, EstadoPedido, DetallePedido
from pedidos.services import ZERO

class CarritoDetailViewTest(BaseTestCase):
    
    def test_get_muestra_carrito(self):
        
        self.client.force_login(self.usuario)
        
        url = reverse("pedidos:carrito")
        
        response = self.client.get(url)
        
        self.assertEqual(
            response.status_code,
            200
        )
        
    def test_carrito_corresponde_al_usuario_autenticado(self):
        
        otro_usuario = Usuario.objects.create_user(
            email="otro@test.com",
            password="123456789",
            first_name="Otro",
            last_name="Usuario",
        )
        
        otro_cliente = Cliente.objects.create(
            usuario=otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        otro_pedido = Pedido.objects.create(
            cliente=otro_cliente,
            estado=EstadoPedido.PENDIENTE,
            subtotal=ZERO,
            costo_envio=ZERO,
            total=ZERO,
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse("pedidos:carrito")
        )
        
        self.assertEqual(
            response.context["pedido"],
            self.pedido
        )
        
        self.assertNotEqual(
            response.context["pedido"],
            otro_pedido
        )
        
    def test_carrito_requiere_autenticacion(self):
        
        carrito_url = reverse("pedidos:carrito")
        
        login_url = reverse("usuarios:login")
        
        response = self.client.get(carrito_url)
        
        self.assertRedirects(
            response,
            f"{login_url}?next={carrito_url}"
        )
        
class AgregarAlCarritoViewTest(BaseTestCase):
    
    def test_agregar_producto_correctamente(self):
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={
                    "pk": self.producto.pk
                }
            ),
            data={
                "cantidad": 2
            }
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        detalle = DetallePedido.objects.get(
            pedido=self.pedido,
            producto=self.producto
        )
        
        self.assertEqual(
            detalle.cantidad,
            2
        )
        
        messages = list(
            get_messages(response.wsgi_request)
        )
        
        self.assertEqual(
            len(messages),
            1
        )
        
        self.assertEqual(
            str(messages[0]),
            "Producto agregado al carrito."
        )
        
    def test_agregar_producto_formulario_invalido(self):
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={
                    "pk": self.producto.pk
                }
            ),
            data={
                "cantidad": 0
            }
        )
        
        self.assertRedirects(
            response,
            reverse(
                "catalogo:detalle_producto",
                kwargs={
                    "pk": self.producto.pk
                }
            )
        )
        
        self.assertFalse(
            DetallePedido.objects.filter(
                pedido=self.pedido,
                producto=self.producto
            ).exists()
        )
        
    def test_agregar_producto_stock_insuficiente(self):
        
        self.client.force_login(self.usuario)
        
        cantidad = self.producto.stock + 1
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={
                    "pk": self.producto.pk
                }
            ),
            data={
                "cantidad": cantidad
            }
        )
        
        self.assertRedirects(
            response,
            reverse(
                "catalogo:detalle_producto",
                kwargs={
                    "pk": self.producto.pk
                }
            )
        )
        
        self.assertFalse(
            DetallePedido.objects.filter(
                pedido=self.pedido,
                producto=self.producto
            ).exists()
        )
        
    def test_agregar_producto_requiere_autenticacion(self):
        
        response = self.client.post(
            reverse(
                "pedidos:agregar_producto",
                kwargs={
                    "pk": self.producto.pk
                }
            ),
            data={
                "cantidad": 2
            }
        )
        
        carrito_url = reverse(
            "pedidos:agregar_producto",
            kwargs={
                "pk": self.producto.pk
            }
        )
        
        login_url = reverse("usuarios:login")
        
        self.assertRedirects(
            response,
            f"{login_url}?next={carrito_url}"
        )
        
        self.assertFalse(
            DetallePedido.objects.filter(
                pedido=self.pedido,
                producto=self.producto
            ).exists()
        )

class ActualizarCantidadViewTest(BaseTestCase):
    
    def test_actualizar_cantidad_correctamente(self):
        
        detalle = self.crear_detalle(
            cantidad=1
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:actualizar_cantidad",
                kwargs={
                    "detalle_id": detalle.pk
                }
            ),
            data={
                "cantidad": 3
            }
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        detalle.refresh_from_db()
        
        self.assertEqual(
            detalle.cantidad,
            3
        )
        
    def test_actualizar_cantidad_cero_elimina_detalle(self):
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse(
                "pedidos:actualizar_cantidad",
                kwargs={
                    "detalle_id": detalle.pk
                }
            ),
            data={
                "cantidad": 0
            }
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        self.assertFalse(
            DetallePedido.objects.filter(
                pk=detalle.pk
            ).exists()
        )
        
    def test_actualizar_cantidad_stock_insuficiente(self):
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        self.client.force_login(self.usuario)
        
        cantidad = self.producto.stock + 1
        
        response = self.client.post(
            reverse(
                "pedidos:actualizar_cantidad",
                kwargs={
                    "detalle_id": detalle.pk
                }
            ),
            data={
                "cantidad": cantidad
            }
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        detalle.refresh_from_db()
        
        self.assertEqual(
            detalle.cantidad,
            2
        )
        
    def test_actualizar_cantidad_requiere_autenticacion(self):
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        detalle_url = reverse(
            "pedidos:actualizar_cantidad",
            kwargs={
                "detalle_id": detalle.pk
            }
        )
        
        login_url = reverse("usuarios:login")
        
        response = self.client.post(
            detalle_url,
            data={
                "cantidad": 3
            }
        )
        
        self.assertRedirects(
            response,
            f"{login_url}?next={detalle_url}"
        )
        
        detalle.refresh_from_db()
        
        self.assertEqual(
            detalle.cantidad,
            2
        )
