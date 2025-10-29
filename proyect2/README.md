
  
Analizador sintáctico predictivo descendente LL(1) para lenguaje Python, continuación del analizador léxico del Proyecto 1.

 Descripción general

El analizador recibe como entrada el archivo salida.txt generado por el analizador léxico (analizador.py) y verifica que la secuencia de tokens cumpla con la gramática libre de contexto definida en sintactico.py.

El objetivo es validar estructuras como declaraciones de clases, funciones, condicionales, bucles, listas, llamadas, asignaciones y expresiones aritméticas.

 Gramática soportada

La gramática está definida en formato BNF simplificado en la variable rules.
Incluye producciones para:

Estructuras de alto nivel: programa, decl, class_decl, func_decl

Bloques e indentación: uso de tokens TABS (indentación) y ATRAS (dedentación)

Sentencias: if_stmt, while_stmt, for_stmt, print_stmt, return_stmt

Expresiones y operaciones: expresion, termino, factor

Listas y llamadas: lista, args, acceso_llamada

Tipos y asignaciones: tipo, tipo_opc, stmt_id'

Soporta listas, atributos encadenados, expresiones anidadas y bloques dependientes de indentación.

 Estructuras de datos utilizadas

rules: lista de producciones gramaticales

producciones: defaultdict(list) que mapea no terminales a sus producciones

FIRST, FOLLOW: defaultdict(set) para almacenar los conjuntos de primeros y siguientes

tabla: defaultdict(dict) que representa la tabla de parseo LL(1)

pila: lista que actúa como pila de análisis durante el parseo

tokens: lista de diccionarios que representan los tokens del archivo léxico

 Características del parser

Implementa un analizador predictivo descendente LL(1)

Construye automáticamente los conjuntos FIRST y FOLLOW

Genera y utiliza una tabla LL(1) para decidir qué producción aplicar

Maneja correctamente ε-producciones (vacías)

Detecta y reporta errores sintácticos detallados, indicando:

Línea y columna del error

Token encontrado y esperado

Errores específicos de indentación o dedentación

 Algoritmos principales

primeros(simbolo)
Calcula los conjuntos FIRST de cada símbolo recursivamente.

calcular_first() / calcular_follow()
Iteran hasta alcanzar un punto fijo para todos los no terminales.

construir_tabla()
Llena la tabla LL(1) combinando los conjuntos FIRST y FOLLOW.

analizador_sintactico(tokens, tabla)
Ejecuta el algoritmo de matching:

Compara el tope de la pila con el token actual.

Si es un terminal, hace pop y avanza.

Si es no terminal, busca la producción en la tabla LL(1).

Reporta errores si no hay coincidencia.

 Ejecución

Ejecutar el analizador léxico:

    python analizador.py


→ Genera salida.txt con los tokens.

Ejecutar el analizador sintáctico:

      python sintactico.py


Si no hay errores, mostrará:

 Análisis sintáctico completado sin errores.

📄 Créditos

Desarrollado como parte del Proyecto 2: Analizador Sintáctico LL(1)
Curso: Fundamentos de Diseño de Software / Paradigmas de Programación
