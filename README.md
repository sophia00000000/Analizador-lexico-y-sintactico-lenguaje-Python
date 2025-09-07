# Proyecto 1: Analizador Léxico Lenguaje Python

El objetivo para este proyecto es tomar un código fuente escrito en python y realizar un
análisis léxico sobre dicho código. Debe implementar un programa en Python que reciba un
archivo como entrada y devuelva un archivo como salida.


## Gramática

### Alfabeto (Σ)

Letras y guion bajo: a-z, A-Z, _
Dígitos: 0-9
Espacios en blanco: espacio, tabulador, salto de línea (isspace())
Comillas: ' y "
Símbolos reconocidos: ( ) : . = == != -> + - * / , > <
'#' (para comentarios)
Cualquier otro carácter no listado → produce error léxico.

### Estados (Q)

Se implementa la máquina de estados finitos, el cual hace la transición de estados dependiendo de lo que lea en el archivo .py

Q = { q0, q_id, q_num, q_string, q_sym2, q_error }

- <code>q0:</code> se empieza la bisqueda de los tokens (estado inicial).
- <code>q_id:</code> leyendo identificador / palabra reservada.
- <code>q_num:</code> lectura de número entero.
- <code>q_string:</code> dentro de una cadena (entre comillas).
- <code>q_sym2:</code> lectura de un posible símbolo de 2 caracteres, se comprueba si viene otro '=' en el código la comprobación de pares se hace instantáneamente.
- <code>q_error:</code> avisa de un error léxico (estado de error).

###  Estado inicial

q0 (estadoinicial y de aceptación por los comentarios)

### Estados de aceptación (F)

F = { q0, q_id, q_num, q_string }

Aquí, todos los estados pueden llevar a aceptación después de procesar su lexema, excepto que si hay un error en q_string (cadena no cerrada) o símbolo desconocido en q0, se produce error.

### Funciónes de transición (δ)

Desde q0:

- isspace() → q0 (ignorar)
- '#' → fin de línea (aceptación implícita, termina lectura)
- Letra o _ → q_id
- Dígito → q_num
- Comillas (' o ") → q_string
- Símbolo de 2 caracteres (en SIMBOLOS) → emitir token y permanecer en q0
- Símbolo de 1 carácter (en SIMBOLOS) → emitir token y permanecer en q0
- Otro → error léxico

<br>

Desde q_id:

- Mientras isalnum() o _ → permanecer en q_id
- Otro → emitir token (reservada o identificador) y regresar a q0 (sin consumir el carácter que rompió la secuencia)

<br>

Desde q_num:

- Mientras dígito → permanecer en q_num
- Otro → emitir token <tk_entero> y regresar a q0 (sin consumir el carácter que rompió la secuencia)

<br>

Desde q_string:

- Mientras no se cierre la comilla → permanecer en q_string
- Si se encuentra la misma comilla → emitir token <tk_cadena> y regresar a q0
- Si fin de línea sin cerrar → error léxico

<br>


## Explicación del código

