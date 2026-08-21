from .base import BaseTestCase
from pedidos.services import (
    crear_pedido, 
    confirmar_pedido,
    asignar_direccion_pedido,
    obtener_pedido_pendiente,
    iniciar_pago,
    procesar_pago,
    aplicar_pago_aprobado,
    calcular_subtotal,
    calcular_total,
    confirmar_pago,
    enviar_pedido,
)
from pedidos.models import (Pedido, 
    EstadoPedido, 
    DetallePedido,
    Pago,
    EstadoPago,
)
from pedidos.exceptions import (
    StockInsuficienteError,
    EstadoPedidoInvalidoError,
    PedidoVacioError,
    PedidoSinDireccionError,
    DireccionPedidoInvalidaError,
    EstadoPagoInvalidoError,
)
from catalogo.models import Producto
from clientes.models import Direccion, Cliente

from decimal import Decimal

from django.db.models import ProtectedError
from django.db import IntegrityError

from unittest.mock import patch

class PedidosTestCase(BaseTestCase):
    
    #-----------------------------------------
    # crear_pedido()
    #-----------------------------------------
    def test_crear_pedido_retorna_pedido_existente(self):
        
        # Act
        pedido = crear_pedido(self.cliente)
        
        # Assert
        self.assertEqual(
            pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            Pedido.objects.filter(
                cliente=self.cliente,
                estado=EstadoPedido.PENDIENTE
            ).count(),
            1
        )
    
    def test_crear_pedido_crea_un_nuevo_pedido(self):
        
        # Arrange
        self.pedido.estado = EstadoPedido.ENTREGADO
        
        self.pedido.save(update_fields=["estado"])
        
        # Act
        pedido = crear_pedido(self.cliente)
        
        # Assert
        self.assertNotEqual(
            pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PENDIENTE
        )
        
    def test_crear_pedido_crea_nuevo_si_no_hay_pendiente(self):
        
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["estado"])
        
        nuevo_pedido = crear_pedido(self.cliente)
        
        self.assertNotEqual(
            nuevo_pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            nuevo_pedido.cliente,
            self.cliente
        )
        
        self.assertEqual(
            nuevo_pedido.estado,
            EstadoPedido.PENDIENTE
        )
        
    def test_crear_pedido_crea_nuevo_despues_de_confirmar(self):
        
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
        
        self.crear_detalle(
            cantidad=2
        )
        
        confirmar_pedido(self.pedido)
        
        nuevo_pedido = crear_pedido(self.cliente)
        
        self.assertNotEqual(
            nuevo_pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION
        )
        
        self.assertEqual(
            nuevo_pedido.estado,
            EstadoPedido.PENDIENTE
        )
    
    #-----------------------------------------
    # confirmar_pedido()
    #-----------------------------------------
    def test_confirmar_pedido_lanza_error_si_esta_vacio(self):
        
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
        
        # Act + Assert
        with self.assertRaises(PedidoVacioError):
            confirmar_pedido(self.pedido)
    
    def test_confirmar_pedido_lanza_error_si_no_hay_stock(self):
        
        # Arrange
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
        
        self.crear_detalle(cantidad=25)
        
        # Act + Assert
        with self.assertRaises(StockInsuficienteError):
            confirmar_pedido(self.pedido)
            
        self.producto.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            20
        )
    
    def test_confirmar_pedido_lanza_error_si_estado_no_es_pendiente(self):
        
        # Arrange
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
        
        self.crear_detalle(cantidad=2)
        
        self.pedido.estado = EstadoPedido.CANCELADO
        
        self.pedido.save(update_fields=["estado"])
        
        # Act
        with self.assertRaises(EstadoPedidoInvalidoError):
            confirmar_pedido(self.pedido)
            
        # Assert
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.CANCELADO
        )
    
    def test_confirmar_pedido_actualiza_estado(self):
        
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
        
        # Arrange
        self.crear_detalle(cantidad=2)
        
        # Act
        pedido = confirmar_pedido(self.pedido)
        
        # Assert
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PREPARACION
        )
    
    def test_confirmar_pedido_descuenta_stock(self):
        
        # Arrange
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
        
        cantidad = 3
        
        self.crear_detalle(
            cantidad=cantidad
        )
        
        stock_inicial = self.producto.stock
        
        # Act
        confirmar_pedido(self.pedido)
        
        # Assert
        self.producto.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_inicial - cantidad
        )
    
    def test_confirmar_pedido_actualiza_totales(self):
        
        # Arrange
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
        
        self.crear_detalle(cantidad=2)
        
        self.pedido.costo_envio = Decimal("8_000.00")
        self.pedido.save(update_fields=["costo_envio"])
        
        # Act
        pedido = confirmar_pedido(self.pedido)
        
        # Assert
        pedido.refresh_from_db()
        
        self.assertEqual(
            pedido.subtotal,
            Decimal("40_000.00")
        )
        
        self.assertEqual(
            pedido.total,
            Decimal("48_000.00")
        )

    def test_confirmar_pedido_estado_invalido_no_modifica_stock(self):
        
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
        
        detalle = self.crear_detalle(
            cantidad=2
        )
        
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save()
        
        stock_inicial = self.producto.stock
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            confirmar_pedido(self.pedido)
            
        self.producto.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_inicial
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
        
    def test_crear_pedido_reutiliza_pedido_pendiente(self):
        
        pedido = crear_pedido(self.cliente)
        
        self.assertEqual(
            pedido.pk,
            self.pedido.pk
        )
        
        self.assertEqual(
            Pedido.objects.filter(
                cliente=self.cliente,
                estado=EstadoPedido.PENDIENTE
            ).count(),
            1
        )
        
    def test_confirmar_pedido_revierte_stock_si_falla(self):
        
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
        
        producto_2 = Producto.objects.create(
            categoria=self.categoria,
            marca=self.marca,
            sku="LAB002",
            nombre="Labial 2",
            precio_compra=Decimal("10.00"),
            precio_venta=Decimal("20.00"),
            stock=1,
        )
        
        self.crear_detalle(
            producto=self.producto,
            cantidad=2,
        )
        
        self.crear_detalle(
            producto=producto_2,
            cantidad=2,
        )
        
        stock_producto_1 = self.producto.stock
        stock_producto_2 = producto_2.stock
        
        with self.assertRaises(StockInsuficienteError):
            confirmar_pedido(self.pedido)
            
        self.producto.refresh_from_db()
        producto_2.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.producto.stock,
            stock_producto_1
        )
        
        self.assertEqual(
            producto_2.stock,
            stock_producto_2
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE
        )
        
    def test_confirmar_pedido_fallido_no_modifica_datos_del_pedido(self):
        
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
        
        self.crear_detalle(
            cantidad=21
        )
        
        estado_original = self.pedido.estado
        subtotal_original = self.pedido.subtotal
        total_original = self.pedido.total
        
        with self.assertRaises(StockInsuficienteError):
            confirmar_pedido(self.pedido)
            
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            estado_original
        )
        
        self.assertEqual(
            self.pedido.subtotal,
            subtotal_original
        )
        
        self.assertEqual(
            self.pedido.total,
            total_original
        )
        
    def test_confirmar_pedido_sin_direccion_lanza_error(self):
        self.crear_detalle()
        
        with self.assertRaises(PedidoSinDireccionError):
            confirmar_pedido(self.pedido)
            
    def test_confirmar_pedido_con_direccion_se_confirma(self):
        self.crear_detalle()
        
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
        self.pedido.save(update_fields=["direccion_envio"])
        
        pedido = confirmar_pedido(self.pedido)
        
        self.assertEqual(
            pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_confirmar_pedido_con_direccion_de_otro_cliente_lanza_error(self):
        self.crear_detalle()
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="3117654321",
        )
        
        otra_direccion = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Calle 50 # 60-70",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = otra_direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        with self.assertRaises(DireccionPedidoInvalidaError):
            confirmar_pedido(self.pedido)

    def test_asignar_direccion_pedido_asigna_direccion_del_cliente(self):
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        asignar_direccion_pedido(
            pedido=self.pedido,
            direccion=direccion,
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.direccion_envio,
            direccion,
        )
        
    def test_asignar_direccion_pedido_de_otro_cliente_lanza_error(self):
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="987654321",
            telefono="300986432"
        )
        
        direccion = Direccion.objects.create(
            cliente=otro_cliente,
            nombre="Casa",
            direccion="Calle 50 # 10-20",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=True,
        )
        
        with self.assertRaises(DireccionPedidoInvalidaError):
            asignar_direccion_pedido(
                pedido=self.pedido,
                direccion=direccion,
            )
            
    def test_asignar_direccion_pedido_no_pendiente_lanza_error(self):
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["estado"])
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            asignar_direccion_pedido(
                pedido=self.pedido,
                direccion=direccion,
            )
            
    def test_confirmar_pedido_con_direccion_conserva_direccion(self):
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
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        confirmar_pedido(self.pedido)
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.direccion_envio_id,
            direccion.pk,
        )
        
    def test_confirmar_pedido_conserva_direccion_seleccionada(self):
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
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        confirmar_pedido(self.pedido)
        
        direccion.direccion = "Carrera 50 # 80-90"
        direccion.save(update_fields=["direccion"])
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.direccion_envio_id,
            direccion.pk
        )
        
    def test_no_se_puede_eliminar_direccion_usada_por_pedido(self):
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
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        with self.assertRaises(ProtectedError):
            direccion.delete()
            
    def test_asignar_direccion_pedido_reemplaza_direccion_anterior(self):
        direccion_anterior = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Calle 10 # 20-30",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )

        nueva_direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Oficina",
            direccion="Carrera 50 # 80-90",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050002",
            es_principal=False,
        )
        
        self.pedido.direccion_envio = direccion_anterior
        self.pedido.save(update_fields=["direccion_envio"])
        
        asignar_direccion_pedido(
            self.pedido,
            nueva_direccion,
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.direccion_envio_id,
            nueva_direccion.pk,
        )
        
    def test_obtener_pedido_pendiente_devuelve_pedido_del_cliente(self):
        pedido = crear_pedido(self.cliente)
        
        resultado = obtener_pedido_pendiente(self.cliente)
        
        self.assertEqual(
            resultado.pk,
            pedido.pk,
        )
        
    def test_obtener_pedido_pendiente_no_devuelve_pedido_de_otro_cliente(self):
        self.pedido.delete()
        
        otro_cliente = Cliente.objects.create(
            usuario=self.otro_usuario,
            documento="7891234578",
            telefono="3217894878",
        )
        
        crear_pedido(otro_cliente)
        
        resultado = obtener_pedido_pendiente(self.cliente)
        
        self.assertIsNone(
            resultado,
        )
        
    def test_obtener_pedido_pendiente_no_devuelve_pedido_no_pendiente(self):
        self.pedido.delete()
        
        pedido = crear_pedido(self.cliente)
        
        pedido.estado = EstadoPedido.PREPARACION
        pedido.save(update_fields=["estado"])
        
        resultado = obtener_pedido_pendiente(self.cliente)
        
        self.assertIsNone(
            resultado,
        )
        
    def test_iniciar_pago_pedido_pendiente(self):
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
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        resultado = iniciar_pago(self.pedido)
        
        self.assertIsInstance(
            resultado,
            Pago,
        )
        
    def test_iniciar_pago_pedido_no_pendiente_lanza_error(self):
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["estado"])
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            iniciar_pago(self.pedido)
            
    def test_iniciar_pago_pedido_cancelado_lanza_error(self):
        self.pedido.estado = EstadoPedido.CANCELADO
        self.pedido.save(update_fields=["estado"])
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            iniciar_pago(self.pedido)
            
    def test_iniciar_pago_pedido_vacio_lanza_error(self):
        with self.assertRaises(PedidoVacioError):
            iniciar_pago(self.pedido)
            
    def test_iniciar_pago_pedido_sin_direccion_lanza_error(self):
        self.crear_detalle()
        
        with self.assertRaises(PedidoSinDireccionError):
            iniciar_pago(self.pedido)
            
    def test_iniciar_pago_pedido_valido_crea_pago(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        iniciar_pago(self.pedido)
        
        self.assertTrue(
            Pago.objects.filter(
                pedido=self.pedido
            ).exists()
        )
        
    def test_iniciar_pago_pedido_con_pago_pendiente_devuelve_pago_existente(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago_original = iniciar_pago(self.pedido)
        
        resultado = iniciar_pago(self.pedido)
        
        self.assertEqual(
            resultado.pk,
            pago_original.pk,
        )
        
        self.assertEqual(
            Pago.objects.filter(
                pedido=self.pedido
            ).count(),
            1,
        )
        
    def test_iniciar_pago_pedido_con_pago_aprobado_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        Pago.objects.create(
            pedido=self.pedido,
            estado=EstadoPago.APROBADO,
        )
        
        with self.assertRaises(EstadoPagoInvalidoError):
            iniciar_pago(self.pedido)
           
    def test_iniciar_pago_pedido_con_pago_rechazado_crea_nuevo_pago(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago_rechazado = Pago.objects.create(
            pedido=self.pedido,
            estado=EstadoPago.RECHAZADO,
        )
        
        resultado = iniciar_pago(self.pedido)
        
        self.assertNotEqual(
            resultado.pk,
            pago_rechazado.pk,
        )
        
        self.assertEqual(
            resultado.pedido,
            self.pedido,
        )
        
        self.assertEqual(
            resultado.estado,
            EstadoPago.PENDIENTE,
        )
        
        self.assertEqual(
            Pago.objects.filter(
                pedido=self.pedido
            ).count(),
            2,
        )
        
    def test_procesar_pago_con_aprobado_true_cambia_estado_a_aprobado(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        resultado = procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        pago.refresh_from_db()
        
        self.assertEqual(
            resultado,
            True,
        )
        
        self.assertEqual(
            pago.estado,
            EstadoPago.APROBADO,
        )
        
    def test_procesar_pago_con_aprobado_false_cambia_estado_a_rechazado(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        resultado = procesar_pago(
            pago=pago,
            aprobado=False,
        )
        
        pago.refresh_from_db()
        
        self.assertEqual(
            resultado,
            False,
        )
        
        self.assertEqual(
            pago.estado,
            EstadoPago.RECHAZADO,
        )
        
    def test_procesar_pago_aprobado_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        pago.refresh_from_db()
        
        with self.assertRaises(EstadoPagoInvalidoError):
            procesar_pago(
                pago=pago,
                aprobado=False,
            )
            
    def test_procesar_pago_rechazado_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=False,
        )
        
        pago.refresh_from_db()
        
        with self.assertRaises(EstadoPagoInvalidoError):
            procesar_pago(
                pago=pago,
                aprobado=True,
            )
            
    def test_procesar_pago_aprobado_invalido_no_modifica_estado(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        with self.assertRaises(EstadoPagoInvalidoError):
            procesar_pago(
                pago=pago,
                aprobado=False,
            )
            
        pago.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            EstadoPago.APROBADO,
        )
        
    def test_procesar_pago_rechazado_invalido_no_modifica_estado(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=False,
        )
        
        with self.assertRaises(EstadoPagoInvalidoError):
            procesar_pago(
                pago=pago,
                aprobado=True
            )
            
        pago.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            EstadoPago.RECHAZADO,
        )
        
    def test_aplicar_pago_aprobado_cambia_pedido_a_preparacion(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        aplicar_pago_aprobado(pago)
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_aplicar_pago_no_aprobado_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        with self.assertRaises(EstadoPagoInvalidoError):
            aplicar_pago_aprobado(pago)
            
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_aplicar_pago_aprobado_pedido_no_pendiente_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        self.pedido.estado = EstadoPedido.ENVIADO
        self.pedido.save(update_fields=["estado"])
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            aplicar_pago_aprobado(pago)
            
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.ENVIADO,
        )
        
    def test_aplicar_pago_aprobado_pedido_en_preparacion_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        aplicar_pago_aprobado(pago)
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            aplicar_pago_aprobado(pago)
            
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_aplicar_pago_aprobado_no_modifica_totales_pedido(self):
        self.crear_detalle(
            cantidad=2,
            precio_unitario=Decimal("20_000.00"),
        )
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        
        subtotal = calcular_subtotal(self.pedido)
        
        self.pedido.subtotal = subtotal
        self.pedido.costo_envio = Decimal("5_000.00")
        self.pedido.descuento = Decimal("3_000.00")
        self.pedido.total = calcular_total(
            self.pedido,
            subtotal,
        )
        
        self.pedido.save()
        
        valores_antes = {
            "subtotal": self.pedido.subtotal,
            "costo_envio": self.pedido.costo_envio,
            "descuento": self.pedido.descuento,
            "total": self.pedido.total,
        }
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        aplicar_pago_aprobado(pago)
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
        self.assertEqual(
            self.pedido.subtotal,
            valores_antes["subtotal"],
        )
        
        self.assertEqual(
            self.pedido.costo_envio,
            valores_antes["costo_envio"],
        )
        
        self.assertEqual(
            self.pedido.descuento,
            valores_antes["descuento"],
        )
        
        self.assertEqual(
            self.pedido.total,
            valores_antes["total"],
        )
        
    def test_procesar_pago_rechazado_no_modifica_estado_pedido(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        resultado = procesar_pago(
            pago=pago,
            aprobado=False
        )
        
        self.assertFalse(resultado)
        
        self.pedido.refresh_from_db()
        pago.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            EstadoPago.RECHAZADO,
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_aplicar_pago_aprobado_devuelve_true(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        resultado = aplicar_pago_aprobado(pago)
        
        self.assertTrue(resultado)
        
    def test_aplicar_pago_aprobado_no_modifica_pago(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        cantidad_pagos_antes = Pago.objects.filter(
            pedido=self.pedido
        ).count()
        
        estado_pago_antes = pago.estado
        
        aplicar_pago_aprobado(pago)
        
        pago.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            estado_pago_antes,
        )
        
        self.assertEqual(
            Pago.objects.filter(
                pedido=self.pedido
            ).count(),
            cantidad_pagos_antes,
        )
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_confirmar_pago_aprobado_actualiza_pago_y_pedido(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        resultado = confirmar_pago(
            pago=pago,
            aprobado=True,
        )
        
        pago.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertTrue(resultado)
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_confirmar_pago_rechazado_no_prepara_pedido(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        resultado = confirmar_pago(
            pago=pago,
            aprobado=False,
        )
        
        pago.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertFalse(resultado)
        
        self.assertEqual(
            pago.estado,
            EstadoPago.RECHAZADO,
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_confirmar_pago_si_falla_aplicar_pago_hace_rollback(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        with patch(
            "pedidos.services.pagos.aplicar_pago_aprobado",
            side_effect=EstadoPedidoInvalidoError(
                "Error simulado."
            ),
        ):
            with self.assertRaises(EstadoPedidoInvalidoError):
                confirmar_pago(
                    pago=pago,
                    aprobado=True,
                )
                
        pago.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            EstadoPago.PENDIENTE,
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_confirmar_pago_con_pago_aprobado_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=True,
        )
        
        with self.assertRaises(EstadoPagoInvalidoError):
            confirmar_pago(
                pago=pago,
                aprobado=True
            )
            
        pago.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            EstadoPago.APROBADO,
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_confirmar_pago_con_pago_rechazado_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago,
            aprobado=False,
        )
        
        with self.assertRaises(EstadoPagoInvalidoError):
            confirmar_pago(
                pago=pago,
                aprobado=True,
            )
            
        pago.refresh_from_db()
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            pago.estado,
            EstadoPago.RECHAZADO,
        )
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PENDIENTE,
        )
        
    def test_iniciar_pago_pedido_con_pago_rechazado_crea_nuevo_pago(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        primer_pago = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=primer_pago,
            aprobado=False,
        )
        
        segundo_pago = iniciar_pago(self.pedido)
        
        self.assertNotEqual(
            segundo_pago.pk,
            primer_pago.pk,
        )
        
        self.assertEqual(
            segundo_pago.pedido,
            self.pedido,
        )
        
        self.assertEqual(
            segundo_pago.estado,
            EstadoPago.PENDIENTE,
        )
        
        self.assertEqual(
            Pago.objects.filter(
                pedido=self.pedido
            ).count(),
            2,
        )
        
    def test_iniciar_pago_con_pago_pendiente_no_crea_otro_pago(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        primer_pago = iniciar_pago(self.pedido)
        
        segundo_pago = iniciar_pago(self.pedido)
        
        self.assertEqual(
            segundo_pago.pk,
            primer_pago.pk,
        )
        
        self.assertEqual(
            Pago.objects.filter(
                pedido=self.pedido,
                estado=EstadoPago.PENDIENTE,
            ).count(),
            1,
        )
        
    def test_iniciar_pago_con_pago_rechazado_y_pendiente_devuelve_pendiente(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago_rechazado = iniciar_pago(self.pedido)
        
        procesar_pago(
            pago=pago_rechazado,
            aprobado=False,
        )
        
        pago_pendiente = iniciar_pago(self.pedido)
        
        resultado = iniciar_pago(self.pedido)
        
        self.assertEqual(
            resultado.pk,
            pago_pendiente.pk,
        )
        
        self.assertEqual(
            resultado.estado,
            EstadoPago.PENDIENTE,
        )
        
        self.assertNotEqual(
            resultado.pk,
            pago_rechazado.pk,
        )
        
    def test_no_puede_existir_mas_de_un_pago_pendiente_por_pedido(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.save(update_fields=["direccion_envio"])
        
        pago = iniciar_pago(self.pedido)
        
        with self.assertRaises(IntegrityError):
            Pago.objects.create(
                pedido=self.pedido,
                estado=EstadoPago.PENDIENTE,
            )
            
    def test_iniciar_pago_pedido_en_preparacion_lanza_error(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["direccion_envio", "estado"])
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            iniciar_pago(self.pedido)
            
    def test_aplicar_pago_aprobado_pedido_no_pendiente_no_cambia_estado(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["direccion_envio", "estado"])
        
        pago = Pago.objects.create(
            pedido=self.pedido,
            estado=EstadoPago.APROBADO,
        )
        
        with self.assertRaises(EstadoPedidoInvalidoError):
            aplicar_pago_aprobado(pago)
            
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.PREPARACION,
        )
        
    def test_enviar_pedido_preparacion_cambia_estado_a_enviado(self):
        self.crear_detalle()
        
        direccion = Direccion.objects.create(
            cliente=self.cliente,
            nombre="Casa",
            direccion="Cra 10",
            ciudad="Medellín",
            departamento="Antioquia",
            codigo_postal="050001",
            es_principal=True,
        )
        
        self.pedido.direccion_envio = direccion
        self.pedido.estado = EstadoPedido.PREPARACION
        self.pedido.save(update_fields=["direccion_envio", "estado"])
        
        resultado = enviar_pedido(self.pedido)
        
        self.assertTrue(resultado)
        
        self.pedido.refresh_from_db()
        
        self.assertEqual(
            self.pedido.estado,
            EstadoPedido.ENVIADO,
        )
            