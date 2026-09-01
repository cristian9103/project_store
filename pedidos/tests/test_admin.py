from django.contrib import admin
from django.test import RequestFactory
from unittest.mock import patch

from pedidos.models import EstadoPedido, Pedido
from pedidos.admin import PedidoAdmin
from pedidos.tests import BaseTestCase
from pedidos.exceptions import EstadoPedidoInvalidoError
from clientes.models import Cliente

from pedidos.services import ZERO

class PedidoAdminTestCase(BaseTestCase):
    
    def test_enviar_pedidos_seleccionados_cambia_todos_a_enviado(self):
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["estado"])
        
        cliente_2 = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        pedido_2 = Pedido.objects.create(
            cliente=cliente_2,
            estado=EstadoPedido.PREPARACION,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        queryset = Pedido.objects.filter(
            pk__in=[
                self.pedido.pk,
                pedido_2.pk,
            ]
        )
        
        request = RequestFactory().get("/admin/pedidos/pedido/")
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        with patch.object(
            pedido_admin,
            "message_user",
        ):   
            pedido_admin.enviar_pedidos(
                request,
                queryset,
            )
        
        self.pedido.refresh_from_db()
        pedido_2.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.ENVIADO,
        )
        
        self.assertEqual(
            pedido_2.estado,
            EstadoPedido.ENVIADO,
        )
        
    def test_enviar_pedidos_seleccionados_con_un_pedido_invalido_no_cambia_ninguno(self):
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["estado"])
        
        cliente_2 = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        pedido_2 = Pedido.objects.create(
            cliente=cliente_2,
            estado=EstadoPedido.PENDIENTE,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        queryset = Pedido.objects.filter(
            pk__in=[
                self.pedido.pk,
                pedido_2.pk,
            ]
        )
        
        request = RequestFactory().get("/admin/pedidos/pedido/")
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        with patch.object(
            pedido_admin,
            "message_user",
        ):   
            pedido_admin.enviar_pedidos(
                request,
                queryset,
            )
        
        self.pedido.refresh_from_db()
        pedido_2.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
        self.assertEqual(
            pedido_2.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_enviar_pedidos_esta_registrada_como_accion(self):
        request = RequestFactory().get(
            "/admin/pedidos/pedido"
        )
        
        request.user = self.usuario
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        acciones = dict(
            pedido_admin.get_actions(request)
        )
        
        self.assertIn(
            "enviar_pedidos",
            acciones,
        )
        
    def test_entregar_pedidos_seleccionados_cambia_todos_a_entregado(self):
        self.pedido.estado = EstadoPedido.ENVIADO
        self.pedido.save(update_fields=["estado"])
        
        cliente_2 = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        pedido_2 = Pedido.objects.create(
            cliente=cliente_2,
            estado=EstadoPedido.ENVIADO,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        queryset = Pedido.objects.filter(
            pk__in=[
                self.pedido.pk,
                pedido_2.pk,
            ]
        )
        
        request = RequestFactory().get(
            "/admin/pedidos/pedido/"
        )
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        with patch.object(
            pedido_admin,
            "message_user",
        ):
            pedido_admin.entregar_pedidos(
                request,
                queryset,
            )
            
        self.pedido.refresh_from_db()
        pedido_2.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.ENTREGADO,
        )
        
        self.assertEqual(
            pedido_2.estado,
            EstadoPedido.ENTREGADO,
        )
        
    def test_entregar_pedidos_seleccionados_con_un_pedido_invalido_no_cambia_ninguno(self):
        self.pedido.estado = EstadoPedido.ENVIADO
        self.pedido.save(update_fields=["estado"])
        
        cliente_2 = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        pedido_2 = Pedido.objects.create(
            cliente=cliente_2,
            estado=EstadoPedido.PREPARACION,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        queryset = Pedido.objects.filter(
            pk__in=[
                self.pedido.pk,
                pedido_2.pk,
            ]
        )
        
        request = RequestFactory().get(
            "/admin/pedidos/pedido/"
        )
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        with patch.object(
            pedido_admin,
            "message_user",
        ):
            pedido_admin.entregar_pedidos(
                request,
                queryset,
            )
            
        self.pedido.refresh_from_db()
        pedido_2.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.ENVIADO,
        )
        
        self.assertEqual(
            pedido_2.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_entregar_pedidos_esta_registrada_como_accion(self):
        request = RequestFactory().get(
            "/admin/pedidos/pedido/"
        )
        
        request.user = self.usuario
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        acciones = dict(
            pedido_admin.get_actions(request)
        )
        
        self.assertIn(
            "entregar_pedidos",
            acciones,
        )
        
    def test_cancelar_pedidos_seleccionados_cambia_todos_a_cancelado(self):
        cliente_2 = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )

        pedido_2 = Pedido.objects.create(
            cliente=cliente_2,
            estado=EstadoPedido.PENDIENTE,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )

        queryset = Pedido.objects.filter(
            pk__in=[
                self.pedido.pk,
                pedido_2.pk,
            ]
        )

        request = RequestFactory().get(
            "/admin/pedidos/pedido/"
        )

        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )

        with patch.object(
            pedido_admin,
            "message_user",
        ):
            pedido_admin.cancelar_pedidos(
                request,
                queryset,
            )

        self.pedido.refresh_from_db()
        pedido_2.refresh_from_db()

        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.CANCELADO,
        )

        self.assertEqual(
            pedido_2.estado,
            EstadoPedido.CANCELADO,
        )
        
    def test_cancelar_pedidos_seleccionados_con_un_pedido_invalido_no_cambia_ninguno(self):
        cliente_2 = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3119876543",
        )
        
        pedido_2 = Pedido.objects.create(
            cliente=cliente_2,
            estado=EstadoPedido.ENTREGADO,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
        queryset = Pedido.objects.filter(
            pk__in=[
                self.pedido.pk,
                pedido_2.pk,
            ]
        )
        
        request = RequestFactory().get(
            "/admin/pedidos/pedido/"
        )
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        with patch.object(
            pedido_admin,
            "message_user",
        ):
            with self.assertRaises(EstadoPedidoInvalidoError):
                pedido_admin.cancelar_pedidos(
                    request,
                    queryset,
                )
                
        self.pedido.refresh_from_db()
        pedido_2.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
        self.assertEqual(
            pedido_2.estado,
            EstadoPedido.ENTREGADO,
        )
        
    def test_cancelar_pedidos_esta_registrada_como_accion(self):
        request = RequestFactory().get(
            "/admin/pedidos/pedido/"
        )
        
        request.user = self.usuario
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        acciones = dict(
            pedido_admin.get_actions(request)
        )
        
        self.assertIn(
            "cancelar_pedidos",
            acciones,
        )
        
    def test_buscar_pedido_por_email_del_cliente(self):
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site
        )
        
        queryset = Pedido.objects.all()
        
        request = self.factory.get(
            "/admin/pedidos/pedido/",
            {"q": self.usuario.email},
        )
        
        queryset, use_distinct = pedido_admin.get_search_results(
            request,
            queryset,
            self.usuario.email,
        )
        
        self.assertIn(
            self.pedido,
            queryset,
        )
        
    def test_pedido_admin_filtra_por_estado(self):
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        self.assertIn(
            "estado",
            pedido_admin.list_filter,
        )
