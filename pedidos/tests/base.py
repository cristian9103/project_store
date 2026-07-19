from decimal import Decimal

from django.test import TestCase

from usuarios.models import Usuario
from clientes.models import Cliente
from catalogo.models import Categoria, Marca, Producto
from pedidos.models import Pedido, EstadoPedido, DetallePedido
from pedidos.services import ZERO, calcular_subtotal, calcular_total

class BaseTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="cliente@test.com",
            password="123456789",
            first_name="Cristian",
            last_name="Ramirez",
        )
        
        self.cliente = Cliente.objects.create(
            usuario=self.usuario,
            documento="123456789",
            telefono="3001234567",
            direccion="Calle 123",
        )
        
        self.categoria = Categoria.objects.create(
            nombre="Maquillaje"
        )
        
        self.marca = Marca.objects.create(
            nombre="Maybelline"
        )
        
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            marca=self.marca,
            sku="LAB001",
            nombre="Labial",
            precio_compra=Decimal("12_000"),
            precio_venta=Decimal("20_000"),
            stock=20,
        )
        
        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            estado=EstadoPedido.PENDIENTE,
            subtotal=ZERO,
            costo_envio=ZERO,
            descuento=ZERO,
            total=ZERO,
        )
        
    def crear_detalle(
        self,
        producto=None,
        cantidad=1,
        precio_unitario=None,
    ):
        producto = producto or self.producto

        if precio_unitario is None:
            precio_unitario = producto.precio_venta

        return DetallePedido.objects.create(
            pedido=self.pedido,
            producto=producto,
            precio_unitario=precio_unitario,
            cantidad=cantidad,
        )
        
    def calcular_total_pedido(self):
        subtotal = calcular_subtotal(self.pedido)
        
        return calcular_total(
            self.pedido,
            subtotal
        )
        