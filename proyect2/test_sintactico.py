import pytest
from sintactico import (
    calcular_primeros, calcular_siguientes, construir_tabla,
    analizador_sintactico, PRIMEROS, SIGUIENTES, tabla,
    producciones, no_terminales, terminales
)
from io import StringIO
import sys


class TestCalcularPrimeros:
    
    def test_primeros_no_vacío(self):
        """Verifica que los PRIMEROS no estén vacíos después del cálculo"""
        calcular_primeros()
        assert len(PRIMEROS) > 0, "Los PRIMEROS no fueron calculados"
    
    def test_primeros_contiene_programa(self):
        """Verifica que el símbolo 'programa' tenga PRIMEROS"""
        calcular_primeros()
        assert "programa" in PRIMEROS, "No se calcularon PRIMEROS para 'programa'"
    
    def test_primeros_programa_no_vacio(self):
        """Verifica que PRIMEROS de 'programa' no esté vacío"""
        calcular_primeros()
        assert len(PRIMEROS["programa"]) > 0 or "ε" in PRIMEROS["programa"]


class TestCalcularSiguientes:
    """Pruebas para el cálculo de conjuntos SIGUIENTES"""
    
    def test_siguientes_no_vacío(self):
        """Verifica que los SIGUIENTES no estén vacíos después del cálculo"""
        calcular_primeros()
        calcular_siguientes()
        assert len(SIGUIENTES) > 0, "Los SIGUIENTES no fueron calculados"
    
    def test_siguientes_programa_contiene_fin(self):
        """Verifica que SIGUIENTES de 'programa' contenga '$'"""
        calcular_primeros()
        calcular_siguientes()
        assert "$" in SIGUIENTES["programa"], "$ debe estar en SIGUIENTES de 'programa'"


class TestConstruirTabla:
    """Pruebas para la construcción de la tabla LL(1)"""
    
    def test_tabla_no_vacía(self):
        """Verifica que la tabla LL(1) se construyó correctamente"""
        calcular_primeros()
        calcular_siguientes()
        construir_tabla()
        assert len(tabla) > 0, "La tabla LL(1) no fue construida"
    
    def test_tabla_contiene_programa(self):
        """Verifica que 'programa' tenga entrada en la tabla"""
        calcular_primeros()
        calcular_siguientes()
        construir_tabla()
        assert "programa" in tabla, "'programa' debe estar en la tabla"
    
    def test_tabla_programa_tiene_produccion(self):
        """Verifica que 'programa' tenga al menos una producción en su entrada"""
        calcular_primeros()
        calcular_siguientes()
        construir_tabla()
        assert len(tabla["programa"]) > 0, "programa debe tener producciones en la tabla"


class TestAnalizadorSintactico:
    """Pruebas para el analizador sintáctico"""
    
    def setup_method(self):
        """Configura el analizador para cada prueba"""
        calcular_primeros()
        calcular_siguientes()
        construir_tabla()
    
    def test_token_fin_de_programa(self, capsys):
        """Prueba con un token de fin de programa"""
        tokens = [
            {"tipo": "$", "lexema": "$", "linea": 1, "col": 1}
        ]
        # Captura la salida
        analizador_sintactico(tokens, tabla)
        captured = capsys.readouterr()
        # No debe haber error con solo el token de fin
        assert "Error" not in captured.out or "completado sin errores" in captured.out
    
    def test_error_sintactico_basico(self, capsys):
        """Prueba detección de error sintáctico simple"""
        tokens = [
            {"tipo": "tk_par_izq", "lexema": "(", "linea": 1, "col": 1},
            {"tipo": "$", "lexema": "$", "linea": 1, "col": 2}
        ]
        analizador_sintactico(tokens, tabla)
        captured = capsys.readouterr()
        # Debe haber error sintáctico
        assert "Error" in captured.out
    
    def test_analizador_captura_salida(self, capsys):
        """Verifica que el analizador captura salida correctamente"""
        tokens = [
            {"tipo": "$", "lexema": "$", "linea": 1, "col": 1}
        ]
        analizador_sintactico(tokens, tabla)
        captured = capsys.readouterr()
        assert captured.out != "", "El analizador debe producir salida"


class TestGramatica:
    """Pruebas para la gramática y producciones"""
    
    def test_producciones_no_vacías(self):
        """Verifica que haya producciones cargadas"""
        assert len(producciones) > 0, "No hay producciones cargadas"
    
    def test_no_terminales_no_vacío(self):
        """Verifica que haya no terminales"""
        assert len(no_terminales) > 0, "No hay no terminales"
    
    def test_terminales_no_vacío(self):
        """Verifica que haya terminales"""
        assert len(terminales) > 0, "No hay terminales"
    
    def test_programa_en_producciones(self):
        """Verifica que 'programa' esté definido en las producciones"""
        assert "programa" in producciones, "'programa' debe estar en producciones"
    
    def test_cada_produccion_tiene_alternativas(self):
        """Verifica que cada producción tenga al menos una alternativa"""
        for no_terminal, alternativas in producciones.items():
            assert len(alternativas) > 0, f"'{no_terminal}' debe tener al menos una alternativa"


class TestIntegracion:
    """Pruebas de integración del analizador sintáctico"""
    
    def test_flujo_completo(self, capsys):
        """Prueba el flujo completo de cálculo y análisis"""
        # Calcula PRIMEROS, SIGUIENTES y construye tabla
        calcular_primeros()
        calcular_siguientes()
        construir_tabla()
        
        # Prueba con tokens simples
        tokens = [
            {"tipo": "$", "lexema": "$", "linea": 1, "col": 1}
        ]
        
        analizador_sintactico(tokens, tabla, "programa")
        captured = capsys.readouterr()
        
        # Debe haber alguna salida
        assert len(captured.out) > 0
    
    def test_multiples_tokens(self, capsys):
        """Prueba con múltiples tokens"""
        calcular_primeros()
        calcular_siguientes()
        construir_tabla()
        
        tokens = [
            {"tipo": "class", "lexema": "class", "linea": 1, "col": 1},
            {"tipo": "id", "lexema": "MiClase", "linea": 1, "col": 7},
            {"tipo": "tk_dos_puntos", "lexema": ":", "linea": 1, "col": 14},
            {"tipo": "TABS", "lexema": "    ", "linea": 2, "col": 1},
            {"tipo": "ATRAS", "lexema": "", "linea": 3, "col": 1},
            {"tipo": "$", "lexema": "$", "linea": 3, "col": 1}
        ]
        
        analizador_sintactico(tokens, tabla, "programa")
        captured = capsys.readouterr()
        assert len(captured.out) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
