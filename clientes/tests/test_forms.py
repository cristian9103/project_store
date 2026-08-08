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
        
    def test_formulario_direccion_permite_establecer_principal(self):
        
        form = DireccionForm(
            data={
                "nombre": "Casa",
                "direccion": "Carrera 10 # 20-30",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "",
                "es_principal": True,
            }
        )
        
        self.assertTrue(form.is_valid())
        self.assertTrue(
            form.cleaned_data["es_principal"]
        )
        
    def test_formulario_direccion_es_principal_false_por_defecto(self):
        
        form = DireccionForm(
            data={
                "nombre": "Casa",
                "direccion": "Carrera 10 # 20-30",
                "ciudad": "Medellín",
                "departamento": "Antioquia",
                "codigo_postal": "",
            }
        )
        
        self.assertTrue(form.is_valid())
        
        self.assertFalse(
            form.cleaned_data["es_principal"]
        )
        
    def test_formulario_direccion_rechaza_campos_damasiado_largos(self):
        
        campos = {
            "nombre": 51,
            "direccion": 151,
            "ciudad": 71,
            "departamento": 71,
            "codigo_postal": 21,
        }
        
        datos_base = {
            "nombre": "Casa",
            "direccion": "Carrera 10 # 20-30",
            "ciudad": "Medellín",
            "departamento": "Antioquia",
            "codigo_postal": "",
            "es_principal": False,
        }
        
        for campo, longitud in campos.items():
            
            with self.subTest(campo=campo):
                
                datos = datos_base.copy()
                datos[campo] = "A" * longitud
                
                form = DireccionForm(data=datos)
                
                self.assertFalse(
                    form.is_valid()
                )
                
                self.assertIn(
                    campo,
                    form.errors
                )
