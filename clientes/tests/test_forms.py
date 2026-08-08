from pedidos.tests import BaseTestCase

from clientes.forms import DireccionForm

class DireccionFormTestCase(BaseTestCase):
    
    def test_formulario_direccion_valido(self):
        
        form = DireccionForm(
            data={
                "nombre": "Casa",
                "direccion": "Carrera 10 # 20-30",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "050001",
                "es_principal": False,
            }
        )
        
        self.assertTrue(
            form.is_valid()
        )
