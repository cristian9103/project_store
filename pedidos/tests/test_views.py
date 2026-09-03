from django.urls import reverse
from django.contrib.messages import get_messages

from decimal import Decimal

from zoneinfo import ZoneInfo

from .base import BaseTestCase
from clientes.models import Cliente, Direccion
from usuarios.models import Usuario
from pedidos.models import Pedido, EstadoPedido, DetallePedido
from pedidos.services import ZERO, crear_pedido

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
        
class VaciarCarritoViewTest(BaseTestCase):
    
    def test_vaciar_carrito_correctamente(self):
        
        self.crear_detalle(
            cantidad=2
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("pedidos:vaciar_carrito")
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        self.assertFalse(
            DetallePedido.objects.filter(
                pedido=self.pedido
            ).exists()
        )
        
        self.assertTrue(
            Pedido.objects.filter(
                pk=self.pedido.pk
            ).exists()
        )
        
    def test_vaciar_carrito_requiere_autenticacion(self):
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        carrito_url = reverse(
            "pedidos:vaciar_carrito"
        )
        
        login_url = reverse(
            "usuarios:login"
        )
        
        response = self.client.post(
            carrito_url
        )
        
        self.assertRedirects(
            response,
            f"{login_url}?next={carrito_url}"
        )
        
        self.assertTrue(
            DetallePedido.objects.filter(
                pk=detalle.pk
            ).exists()
        )
        
class ConfirmarPedidoViewTest(BaseTestCase):
    
    def test_confirmar_pedido_correctamente(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(
            update_fields=["direccion_envio"]
        )
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        stock_inicial = self.producto.stock
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("pedidos:confirmar_pedido")
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        self.producto.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_inicial - detalle.cantidad
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION
        )
    
    def test_confirmar_pedido_requiere_autenticacion(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(
            update_fields=["direccion_envio"]
        )
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        stock_inicial = self.producto.stock
        
        confirmar_url = reverse(
            "pedidos:confirmar_pedido"
        )
        
        login_url = reverse(
            "usuarios:login"
        )
        
        response = self.client.post(
            confirmar_url
        )
        
        self.assertRedirects(
            response,
            f"{login_url}?next={confirmar_url}"
        )
        
        self.producto.refresh_from_db()
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_inicial
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE
        )
        
        self.assertTrue(
            DetallePedido.objects.filter(
                pk=detalle.pk
            ).exists()
        )
        
    def test_confirmar_pedido_stock_insuficiente(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(
            update_fields=["direccion_envio"]
        )
        
        cantidad = self.producto.stock + 1
        
        detalle = self.crear_detalle(
            cantidad=cantidad
        )
        
        stock_inicial = self.producto.stock
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("pedidos:confirmar_pedido")
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        self.producto.refresh_from_db()
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_inicial
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE
        )
        
        self.assertTrue(
            DetallePedido.objects.filter(
                pk=detalle.pk
            ).exists()
        )
        
    def test_confirmar_pedido_ya_confirmado_no_descuenta_stock(self):
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 #20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(
            update_fields=["direccion_envio"]
        )
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save()
        
        stock_incial = self.producto.stock
        
        self.client.force_login(self.usuario)
        
        response = self.client.post(
            reverse("pedidos:confirmar_pedido")
        )
        
        self.assertRedirects(
            response,
            reverse("pedidos:carrito")
        )
        
        self.producto.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_incial
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION
        )
        
        self.assertTrue(
            DetallePedido.objects.filter(
                pk=detalle.pk
            ).exists()
        )
        
class CheckoutViewTest(BaseTestCase):
    
    def test_checkout_usuario_autenticado_muestra_pedido_pendiente(self):
        self.client.force_login(self.usuario)
        
        crear_pedido(self.cliente)
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
    def test_checkout_muestra_las_direcciones_del_cliente(self):
        self.client.force_login(self.usuario)
        
        crear_pedido(self.cliente)
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertIn(
            direccion,
            response.context["direcciones"],
        )
        
    def test_checkout_no_muestra_direcciones_de_otro_cliente(self):
        self.client.force_login(self.usuario)
        
        crear_pedido(self.cliente)
        
        direccion_cliente = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        direccion_otro_cliente = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Calle 50 # 60-70",
            ciudad="Bogotá",
            departamento="Cundinamarca",
            codigo_postal="110001",
            es_principal=True,
        )
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        direcciones = response.context["direcciones"]
        
        self.assertIn(
            direccion_cliente,
            direcciones,
        )
        
        self.assertNotIn(
            direccion_otro_cliente,
            direcciones,
        )
        
    def test_checkout_post_asigna_direccion_al_pedido(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "direccion_id": direccion.pk,
            },
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.direccion_envio_id,
            direccion.pk,
        )
        
    def test_checkout_no_puede_asignar_direccion_de_otro_cliente(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        direccion = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Calle 50 # 60-70",
            ciudad="Bogotá",
            departamento="Cundinamarca",
            codigo_postal="110001",
            es_principal=True,
        )
        
        response = self.client.post(
            
            reverse("pedidos:checkout"),
            {
                "direccion_id": direccion.pk,
            },
        )
        
        self.assertEqual(
            response.status_code,
            404,
        )
        
        pedido.refresh_from_db()
        
        self.assertIsNone(
            pedido.direccion_envio_id,
        )
        
    def test_checkout_con_direccion_inexistente_lanza_404(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "direccion_id": 99999,
            },
        )
        
        self.assertEqual(
            response.status_code,
            404,
        )
        
        pedido.refresh_from_db()
        
        self.assertIsNone(
            pedido.direccion_envio_id,
        )
        
    def test_checkout_sin_direccion_no_asigna_direccion(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {}
        )
        
        pedido.refresh_from_db()
        
        self.assertIsNone(
            pedido.direccion_envio_id,
        )
        
    def test_checkout_muestra_direccion_de_envio_seleccionada(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.client.post(
            reverse("pedidos:checkout"),
            {
                "direccion_id": direccion.pk,
            },
        )
        
        response = self.client.get(
            reverse("pedidos:checkout"),
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.direccion_envio_id,
            direccion.pk,
        )
        
        self.assertEqual(
            response.context["pedido"].direccion_envio_id,
            direccion.pk,
        )
        
    def test_checkout_pedido_con_direccion_seleccionada_la_conserva(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        pedido.direccion_envio = direccion
        pedido.save(update_fields=["direccion_envio"])
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        pedido_contexto = response.context["pedido"]
        
        self.assertEqual(
            pedido_contexto.direccion_envio_id,
            direccion.pk,
        )
        
    def test_checkout_post_sin_direccion_muestra_error_del_formulario(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {},
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        form = response.context["form"]
        
        self.assertFalse(
            form.is_valid()
        )
        
        self.assertIn(
            "direccion_id",
            form.errors,
        )
        
    def test_checkout_sin_direccion_muestra_error_en_html(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {},
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            "Selecciona una dirección de envío."
        )
        
    def test_checkout_post_confirma_pedido_con_direccion(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        pedido.direccion_envio = direccion
        pedido.save(update_fields=["direccion_envio"])
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
            },
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
        self.assertEqual(
            pedido.direccion_envio_id,
            direccion.pk,
        )
        
    def test_checkout_confirmar_sin_direccion_muestra_error(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        self.crear_detalle()
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
            },
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            "El pedido necesita una dirección de envío.",
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_checkout_confirmar_pedido_vacio_muestra_error(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        pedido.direccion_envio = direccion
        pedido.save(update_fields=["direccion_envio"])
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
            },
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            "El pedido no tiene productos.",
        )
        
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_checkout_confirmar_stock_insuficiente_muestra_error(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        
        self.crear_detalle(cantidad=21)
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        pedido.direccion_envio = direccion
        pedido.save(update_fields=["direccion_envio"])
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
            },
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            "No hay stock suficiente.",
        )
        
        pedido.refresh_from_db()
        self.producto.refresh_from_db()
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
        self.assertEqual(
            self.producto.stock,
            20,
        )
        
    def test_checkout_confirmacion_exitosa_actualiza_todo(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        
        self.crear_detalle(cantidad=10)
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "direccion_id": direccion.pk,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        pedido.refresh_from_db()
        self.producto.refresh_from_db()
        
        self.assertEqual(
            pedido.cliente_id,
            self.cliente.pk,
        )
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
        self.assertEqual(
            pedido.direccion_envio_id,
            direccion.pk,
        )
        
        self.assertEqual(
            self.producto.stock,
            10,
        )
        
        self.assertEqual(
            pedido.subtotal,
            Decimal("200_000.00"),
        )
        
        self.assertEqual(
            pedido.total,
            Decimal("200_000.00"),
        )
        
    def test_checkout_confirmacion_exitosa_redirige_a_exito(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "direccion_id": direccion.pk,
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
            },
        )
        
        self.assertEqual(
            response.status_code,
            302,
        )
        
        self.assertRedirects(
            response,
            reverse(
                "pedidos:checkout_exito",
                kwargs={"pk": pedido.pk},
            ),
        )
        
    def test_checkout_exito_muestra_pedido_del_cliente(self):
        self.client.force_login(self.usuario)
        
        pedido = crear_pedido(self.cliente)
        
        pedido.estado = EstadoPedido.PREPARACION
        pedido.save(update_fields={"estado"})
        
        response = self.client.get(
            reverse(
                "pedidos:checkout_exito",
                kwargs={"pk": pedido.pk},
            )
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertEqual(
            response.context["pedido"].pk,
            pedido.pk,
        )
        
    def test_checkout_exito_no_muestra_pedido_de_otro_cliente(self):
        self.client.force_login(self.usuario)
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987321654",
            telefono="3217894561",
        )
        
        pedido = crear_pedido(otro_cliente)
        
        pedido.estado = EstadoPedido.PREPARACION
        pedido.save(update_fields=["estado"])
        
        response = self.client.get(
            reverse(
                "pedidos:checkout_exito",
                kwargs={"pk": pedido.pk},
            )
        )
        
        self.assertEqual(
            response.status_code,
            404,
        )
        
    def test_checkout_no_puede_confirmar_pedido_de_otro_cliente(self):
        self.client.force_login(self.usuario)
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987321654",
            telefono="3217894561",
        )
        
        otro_pedido = crear_pedido(otro_cliente)
        
        DetallePedido.objects.create(
            pedido=otro_pedido,
            producto=self.producto,
            precio_unitario=Decimal("20_000.00"),
            cantidad=1,
            subtotal=Decimal("20_000.00"),
        )
        
        direccion = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Calle 20",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=True,
        )
        
        otro_pedido.direccion_envio = direccion
        otro_pedido.save(update_fields=["direccion_envio"])
        
        response = self.client.post(
            reverse("pedidos:checkout"),
            {
                "accion": "confirmar",
                "pedido_id": otro_pedido.pk,
            },
        )
        
        otro_pedido.refresh_from_db()
        
        self.assertEqual(
            otro_pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_checkout_muestra_datos_de_direccion_en_html(self):
        self.client.force_login(self.usuario)
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            "Casa",
        )
        
        self.assertContains(
            response,
            "Calle 10 # 20-30"
        )
        
        self.assertContains(
            response,
            "Medellín"
        )
        
        self.assertContains(
            response,
            "Antioquia",
        )
        
        self.assertContains(
            response,
            "050001",
        )
        
    def test_checkout_muestra_boton_confirmar_pedido(self):
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            "Confirmar pedido",
        )
        
    def test_checkout_muestra_pedido_y_direcciones_del_cliente(self):
        direccion_1 = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
        )

        direccion_2 = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Trabajo",
            direccion="Carrera 40 # 50-60",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
        )
        
        self.client.force_login(self.usuario)
        
        request = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            request.status_code,
            200,
        )
        
        self.assertEqual(
            request.context["pedido"],
            self.pedido
        )
        
        self.assertQuerySetEqual(
            request.context["direcciones"],
            [
                direccion_1.pk,
                direccion_2.pk,
            ],
            transform=lambda direccion: direccion.pk,
            ordered=False,
        )
        
    def test_get_checkout_muestra_pedido_y_direcciones(self):
        direccion_1 = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
        )

        direccion_2 = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Trabajo",
            direccion="Carrera 40 # 50-60",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
        )
        
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertEqual(
            response.context["pedido"],
            self.pedido,
        )
        
        self.assertQuerySetEqual(
            response.context["direcciones"],
            [
                direccion_1.pk,
                direccion_2.pk,
            ],
            transform=lambda direccion: direccion.pk,
            ordered=False
        )
        
    def test_checkout_sin_pedido_pendiente_crea_pedido(self):
        self.pedido.delete()
        
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse("pedidos:checkout")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        pedido = Pedido.objects.get(
            cliente=self.cliente,
            estado=EstadoPedido.PENDIENTE,
        )
        
        self.assertEqual(
            response.context["pedido"],
            pedido,
        )
        
class HistorialViewTest(BaseTestCase):
        
    def test_historial_muestra_los_pedidos_del_cliente(self):
        self.client.force_login(self.usuario)
        
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.subtotal = Decimal("20_000.00")
        self.pedido.total = Decimal("20_000.00")
        self.pedido.save(update_fields=["estado", "subtotal", "total"])
        
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertContains(
            response,
            f"Pedido #{self.pedido.pk}"
        )
        
    def test_historial_no_muestra_pedidos_de_otro_cliente(self):
        self.client.force_login(self.usuario)
        
        pedido_otro_cliente = Pedido.objects.create(
            cliente = Cliente.objects.create(
                usuario=self.otro_usuario,
                documento="987654321",
                telefono="3119876543",
            ),
            estado=EstadoPedido.PREPARACION,
            subtotal=Decimal("30_000.00"),
            costo_envio=ZERO,
            descuento=ZERO,
            total=Decimal("30_000.00"),
        )
        
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertNotContains(
            response,
            f"Pedido #{pedido_otro_cliente.pk}",
        )
        
    def test_historial_muestra_datos_basicos_del_pedido(self):
        self.client.force_login(self.usuario)
        
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            estado=EstadoPedido.PREPARACION,
            subtotal=Decimal("20_000"),
            costo_envio=Decimal("5_000"),
            descuento=ZERO,
            total=Decimal("25_000"),
        )
        
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertContains(
            response,
            f"Pedido #{pedido.pk}",
        )
        
        self.assertContains(
            response,
            pedido.estado.label,
        )
        
        self.assertContains(
            response,
            "25000,00",
        )
        
    def test_historial_muestra_fecha_del_pedido(self):
        self.client.force_login(self.usuario)
        
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            estado=EstadoPedido.PREPARACION,
            subtotal=Decimal("20_000"),
            costo_envio=ZERO,
            descuento=ZERO,
            total=Decimal("20_000"),
        )
        
        pedido.fecha = pedido.fecha.replace(tzinfo=ZoneInfo("America/Bogota"))
        pedido.save(update_fields=["fecha"])
        
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertContains(
            response,
            pedido.fecha.strftime("%d/%m/%Y"),
        )
        
    def test_historial_sin_pedidos_muestra_mensaje(self):
        self.pedido.delete()
        self.client.force_login(self.usuario)
        
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertContains(
            response,
            "Aún no tienes pedidos",
        )
        
    def test_historial_muestra_pedidos_del_mas_reciente_al_mas_antiguo(self):
        self.client.force_login(self.usuario)
        
        pedido_reciente = Pedido.objects.create(
            cliente=self.cliente,
            estado=EstadoPedido.PREPARACION,
            subtotal=Decimal("20_000"),
            costo_envio=ZERO,
            descuento=ZERO,
            total=Decimal("20_000"),
        )
        
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        contenido = response.content.decode()
        
        posicion_reciente = contenido.index(
            f"Pedido #{pedido_reciente.pk}"
        )
        posicion_antiguo = contenido.index(
            f"Pedido #{self.pedido.pk}"
        )
        
        self.assertLess(
            posicion_reciente,
            posicion_antiguo,
        )
        
    def test_historial_pagina_los_pedidos(self):
        self.client.force_login(self.usuario)
        
        for i in range(12):
            Pedido.objects.create(
                cliente=self.cliente,
                estado=EstadoPedido.PREPARACION,
                subtotal=Decimal("10_000"),
                costo_envio=ZERO,
                descuento=ZERO,
                total=Decimal("10_000"),
            )
            
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertTrue(
            response.context["is_paginated"]
        )
        self.assertEqual(
            len(response.context["pedidos"]),
            10,
        )
        
    def test_historial_puede_mostrar_segunda_pagina(self):
        self.client.force_login(self.usuario)
        self.pedido.delete()
        
        pedidos = []
        
        for i in range(12):
            pedidos.append(
                Pedido.objects.create(
                    cliente=self.cliente,
                    estado=EstadoPedido.PREPARACION,
                    subtotal=Decimal("10_000"),
                    costo_envio=ZERO,
                    descuento=ZERO,
                    total=Decimal("10_000"),
                )
            )
            
        response = self.client.get(
            reverse("pedidos:historial"),
            {"page": 2},
        )
        
        self.assertEqual(
            response.status_code,
            200,
        )
        
        self.assertEqual(
            len(response.context["pedidos"]),
            2,
        )
        
    def test_historial_muestra_navegacion_de_paginacion(self):
        self.client.force_login(self.usuario)
        
        for i in range(12):
            Pedido.objects.create(
                cliente=self.cliente,
                estado=EstadoPedido.PREPARACION,
                subtotal=Decimal("10_000"),
                costo_envio=ZERO,
                descuento=ZERO,
                total=Decimal("10_000"),
            )
            
        response = self.client.get(
            reverse("pedidos:historial")
        )
        
        self.assertContains(
            response,
            "Siguiente",
        )
        
        self.assertNotContains(
            response,
            "Anterior",
        )
