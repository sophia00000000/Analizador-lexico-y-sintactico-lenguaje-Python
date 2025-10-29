
# Analizador sintáctico

Analizador sintáctico predictivo descendente LL(1) para lenguaje Python, continuación del analizador léxico del Proyecto 1.

Recibe como entrada el archivo salida.txt generado por el analizador léxico (analizador.py) y verifica que la secuencia de tokens cumpla con la gramática libre de contexto definida.


- Construye los conjuntos FIRST y FOLLOW
  
    `primeros(simbolo)` Calcula los conjuntos FIRST de cada símbolo recursivamente.
    
    `calcular_first()` / `calcular_follow()` Iteran hasta alcanzar un punto fijo para todos los no terminales.
  
- Genera y utiliza una tabla LL(1) para decidir qué producción aplicar
  
    `construir_tabla()` Llena la tabla LL(1) combinando los conjuntos FIRST y FOLLOW.
  
- Ejecuta el algoritmo de matching
  
    `analizador_sintactico(tokens, tabla)` Compara el tope de la pila con el token actual.

    Si es un terminal, hace pop y avanza.

    Si es no terminal, busca la producción en la tabla LL(1).

- Detecta y reporta errores sintácticos, indicando:
  
    - Línea y columna del error
    
    - Token encontrado y esperado
    
    - Errores específicos de indentación o dedentación

### Gramática 

La gramática está definida en formato BNF simplificado.

Incluye producciones para:

- Estructuras de alto nivel: programa, decl, class_decl, func_decl
- Bloques e indentación: uso de tokens TABS (indentación) y ATRAS (dedentación)
- Sentencias: if_stmt, while_stmt, for_stmt, print_stmt, return_stmt
- Expresiones y operaciones: expresion, termino, factor
- Listas y llamadas: lista, args, acceso_llamada
- Tipos y asignaciones: tipo, tipo_opc, stmt_id'
- Soporta listas, atributos encadenados, expresiones anidadas y bloques dependientes de indentación.

- Asignaciones
- Expresiones aritméticas (+ - * / ( ))
- Condicionales if/else
- Ciclos while y for
- listas
- clases
- Bloques indentados
- Identificadores y números (id, tk_entero)

### Estructuras de datos utilizadas

rules: lista de producciones gramaticales

producciones: defaultdict(list) que mapea no terminales a sus producciones

FIRST, FOLLOW: defaultdict(set) para almacenar los conjuntos de primeros y siguientes

tabla: defaultdict(dict) que representa la tabla de parseo LL(1)

pila: lista que actúa como pila de análisis durante el parseo

tokens: lista de diccionarios que representan los tokens del archivo léxico

 



Reporta errores si no hay coincidencia.

### Ejecución

Ejecutar el analizador léxico:

    python analizador.py


→ Genera salida.txt con los tokens.

Ejecutar el analizador sintáctico:

      python sintactico.py


Si no hay errores, mostrará:  Análisis sintáctico completado sin errores.

