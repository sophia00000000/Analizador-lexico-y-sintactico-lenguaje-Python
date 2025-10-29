RESERVADAS = {
    "class", "def", "if", "else", "while", "for", "return", "print",
    "from", "as", "True", "False", "None", "and", "or", "not",
    "in", "is", "break"
}

SIMBOLOS = {
    "(": "tk_par_izq",
    ")": "tk_par_der",
    ":": "tk_dos_puntos",
    ".": "tk_punto",
    "=": "tk_asig",
    "==": "tk_igual",
    "!=": "tk_distinto",
    "->": "tk_ejecuta",
    "+": "tk_suma",
    "-": "tk_resta",
    "*": "tk_mul",
    "/": "tk_div",
    ",": "tk_coma",
    ">": "tk_mayor",
    "<": "tk_menor",
    "[": "tk_cua_izq",
    "]": "tk_cua_der",
    "%": "tk_mod"
}

def analizar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print("Error: archivo no encontrado")
        return []

    tokens = analizar_indents(lineas)
    return tokens

def analizar_indents(lineas):
    tokens = []
    indent_stack = [0]

    for num_linea, linea in enumerate(lineas, start=1):
        # Contar espacios al inicio
        espacios = 0
        while espacios < len(linea) and linea[espacios] in [' ', '\t']:
            espacios += 1

        contenido = linea.strip()
        col_actual = 1

        # Ignorar comentarios o líneas vacías
        if contenido == "" or contenido.startswith("#"):
            continue

        nivel_actual = indent_stack[-1]

        # Verificar cambio de indentación ANTES de tokenizar
        if espacios > nivel_actual:
            indent_stack.append(espacios)
            tokens.append(f"<TABS,{num_linea},{col_actual}>")
        elif espacios < nivel_actual:
            while indent_stack and espacios < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(f"<ATRAS,{num_linea},{col_actual}>")

        # Tokenizar contenido real
        tokens_linea = tokenizar(contenido, num_linea)
        if tokens_linea is None:
            return None
        tokens.extend(tokens_linea)

        # Agregar salto de línea (si la línea no termina con :, (, [ , ,)
        if not linea.strip().endswith((":", ",", "(", "[")):
            tokens.append(f"<tk_nueva_linea,{num_linea},{len(linea)}>")
    
    # Cerrar indentaciones abiertas al final del archivo
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(f"<ATRAS,{num_linea+1},1>")

    return tokens

def tokenizar(linea, num_linea):
    tokens = []
    i = 0
    estado = "q0"

    while i < len(linea):
        ch = linea[i]

        if estado == "q0":
            if ch.isspace():
                i += 1
                continue
            elif ch == "#":
                break
            elif ch.isalpha() or ch == "_":
                estado = "q_id"
                inicio = i
                i += 1
            elif ch.isdigit():
                estado = "q_num"
                inicio = i
                i += 1
            elif ch in {'"', "'"}:
                estado = "q_string"
                inicio = i
                comilla = ch
                i += 1
            elif i + 1 < len(linea) and linea[i:i + 2] in SIMBOLOS:
                tokens.append(f"<{SIMBOLOS[linea[i:i + 2]]},{num_linea},{i + 1}>")
                i += 2
            elif ch in SIMBOLOS:
                tokens.append(f"<{SIMBOLOS[ch]},{num_linea},{i + 1}>")
                i += 1
            else:
                print(f">>> Error léxico(linea:{num_linea},posicion:{i + 1})")
                return None

        elif estado == "q_id":
            while i < len(linea) and (linea[i].isalnum() or linea[i] == "_"):
                i += 1
            lexema = linea[inicio:i]
            if lexema in RESERVADAS:
                tokens.append(f"<{lexema},{num_linea},{inicio + 1}>")
            else:
                tokens.append(f"<id,{lexema},{num_linea},{inicio + 1}>")
            estado = "q0"

        elif estado == "q_num":
            while i < len(linea) and linea[i].isdigit():
                i += 1
            lexema = linea[inicio:i]
            tokens.append(f"<tk_entero,{lexema},{num_linea},{inicio + 1}>")
            estado = "q0"

        elif estado == "q_string":
            while i < len(linea) and linea[i] != comilla:
                i += 1
            if i >= len(linea):
                print(f">>> Error léxico(linea:{num_linea},posicion:{inicio + 1})")
                return None
            lexema = linea[inicio + 1:i]
            tokens.append(f"<tk_cadena,\"{lexema}\",{num_linea},{inicio + 1}>")
            i += 1
            estado = "q0"

    if estado == "q_num":
        lexema = linea[inicio:i]
        tokens.append(f"<tk_entero,{lexema},{num_linea},{inicio + 1}>")
    elif estado == "q_id":
        lexema = linea[inicio:i]
        if lexema in RESERVADAS:
            tokens.append(f"<{lexema},{num_linea},{inicio + 1}>")
        else:
            tokens.append(f"<id,{lexema},{num_linea},{inicio + 1}>")

    return tokens


def guardar_salida(tokens, archivo_salida="salida.txt"):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for t in tokens:
            f.write(t + "\n")

if __name__ == "__main__":
    archivo_entrada = input("Ingrese el nombre del archivo .py a analizar: ")

    tokens = analizar_archivo(archivo_entrada)

    if tokens is not None:
        guardar_salida(tokens)
        print("Análisis léxico completado. Tokens guardados en salida.txt")
