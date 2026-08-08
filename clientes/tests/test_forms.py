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
        
    def test_formulario_direccion_requiere_campos_obligatorios(self):
        
        form = DireccionForm(data={})
        
        self.assertFalse(form.is_valid())
        
        self.assertIn("nombre", form.errors)
        self.assertIn("direccion", form.errors)
        self.assertIn("ciudad", form.errors)
        self.assertIn("departamento", form.errors)
        
    def test_formulario_direccion_codigo_postal_es_opcional(self):
        
        form = DireccionForm(
            data={
                "nombre": "Casa",
                "direccion": "Carrera 10 # 20-30",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "",
                "es_principal": False,
            }
        )
        
        self.assertTrue(form.is_valid())
