from django.contrib import admin

from pedidos.models import EstadoPedido, Pedido
from pedidos.admin import PedidoAdmin
from pedidos.tests import BaseTestCase
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
        
        pedido_admin = PedidoAdmin(
            Pedido,
            admin.site,
        )
        
        pedido_admin.enviar_pedidos(
            None,
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
