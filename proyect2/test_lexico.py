import pytest
from lexico import tokenizar

@pytest.mark.parametrize("entrada, esperado", [
    ("123", ['<tk_entero,123,1,1>']),
    ("456", ['<tk_entero,456,1,1>']),
    ("0", ['<tk_entero,0,1,1>']),
    ("999", ['<tk_entero,999,1,1>']),
])
def test_tokenizar_numeros_parametrizado(entrada, esperado):
    resultado = tokenizar(entrada, num_linea=1)
    assert resultado == esperado


@pytest.mark.parametrize("palabra_reservada", [
    "if", "else", "while", "for", "def", 
    "class", "return", "print", "True", "False"
])
def test_tokenizar_palabras_reservadas_parametrizado(palabra_reservada):
    resultado = tokenizar(palabra_reservada, num_linea=1)
    # La palabra reservada debe aparecer como token
    assert resultado == [f'<{palabra_reservada},1,1>']


@pytest.mark.parametrize("codigo, tokens_esperados", [
    # Sumas
    ("1 + 2", ['<tk_entero,1,1,1>', '<tk_suma,1,3>', '<tk_entero,2,1,5>']),
    
    # Restas
    ("5 - 3", ['<tk_entero,5,1,1>', '<tk_resta,1,3>', '<tk_entero,3,1,5>']),
    
    # Multiplicación
    ("2 * 4", ['<tk_entero,2,1,1>', '<tk_mul,1,3>', '<tk_entero,4,1,5>']),
    
    # División
    ("8 / 2", ['<tk_entero,8,1,1>', '<tk_div,1,3>', '<tk_entero,2,1,5>']),
])
def test_tokenizar_operaciones_parametrizado(codigo, tokens_esperados):
    """
    Test que verifica diferentes operaciones aritméticas
    Cada tupla es un caso de prueba diferente
    """
    resultado = tokenizar(codigo, num_linea=1)
    assert resultado == tokens_esperados


@pytest.mark.parametrize("identificador", [
    "x", "variable", "mi_variable", "_privada", "CamelCase", "numero2"
])
def test_tokenizar_identificadores_parametrizado(identificador):
    """Test que verifica diferentes tipos de identificadores válidos"""
    resultado = tokenizar(identificador, num_linea=1)
    assert resultado == [f'<id,{identificador},1,1>']



def test_tokenizar_numero():
    resultado = tokenizar("123", num_linea=1)
    assert resultado == ['<tk_entero,123,1,1>']


def test_tokenizar_identificador():
    resultado = tokenizar("variable", num_linea=1)
    assert resultado == ['<id,variable,1,1>']


def test_tokenizar_palabra_reservada():
    resultado = tokenizar("if", num_linea=1)
    assert resultado == ['<if,1,1>']


def test_tokenizar_suma():
    resultado = tokenizar("1 + 2", num_linea=1)
    assert resultado == [
        '<tk_entero,1,1,1>',
        '<tk_suma,1,3>',
        '<tk_entero,2,1,5>'
    ]


def test_tokenizar_asignacion():
    resultado = tokenizar("x = 10", num_linea=1)
    assert resultado == [
        '<id,x,1,1>',
        '<tk_asig,1,3>',
        '<tk_entero,10,1,5>'
    ]
