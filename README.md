# Proyecto 1: Analizador Léxico Lenguaje Python

El objetivo para este proyecto es tomar un código fuente escrito en python y realizar un
análisis léxico sobre dicho código. Debe implementar un programa en Python que reciba un
archivo como entrada y devuelva un archivo como salida.


# Gramática

### Alfabeto (Σ)


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



### Estados de aceptación (F)

F = { q_id, q_num, q_string*, q0}

Son estados aceptantes porque una vez que se agotan las letras/dígitos el autómata acepta ese lexema, y en el caso de los strings solo es aceptante cuando se recibe la comilla de cierre;

### Funciónes de transición (δ)

