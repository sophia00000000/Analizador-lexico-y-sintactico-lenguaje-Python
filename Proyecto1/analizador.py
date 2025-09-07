RESERVADAS = {
    "class", "def", "if", "else", "while", "for", "return", "print",
    "import", "from", "as", "True", "False", "None", "and", "or", "not",
    "in", "is", "break", "continue", "pass", "self", "object", "str", "bool", "__init__", "lambda" 
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
    "<": "tk_menor"
}

def analizar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        return [">>> Error léxico(linea:1,posicion:1)"], True

    tokens = []
    hubo_error = False

    for num_linea, linea in enumerate(lineas, start=1):
        resultado = tokenizar(linea, num_linea)

        if isinstance(resultado, tuple) and resultado[0] == "ERROR":
            tokens.extend(resultado[1])   # tokens válidos antes del error
            tokens.append(resultado[2])   # mensaje de error
            hubo_error = True
            break
        else:
            tokens.extend(resultado)

    return tokens, hubo_error

def tokenizar(linea, num_linea):
    tokens = []
    i = 0
    estado = "q0"  # estado inicial

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
            elif i+1 < len(linea) and linea[i:i+2] in SIMBOLOS:
                tokens.append(f"<{SIMBOLOS[linea[i:i+2]]},{num_linea},{i+1}>")
                i += 2
            elif ch in SIMBOLOS:
                tokens.append(f"<{SIMBOLOS[ch]},{num_linea},{i+1}>")
                i += 1
            else:
                error = f">>> Error léxico(linea:{num_linea},posicion:{i+1})"
                return ("ERROR", tokens, error)


        elif estado == "q_id":
            while i < len(linea) and (linea[i].isalnum() or linea[i] == "_"):
                i += 1
            lexema = linea[inicio:i]
            if lexema in RESERVADAS:
                tokens.append(f"<{lexema},{num_linea},{inicio+1}>")
            else:
                tokens.append(f"<id,{lexema},{num_linea},{inicio+1}>")
            estado = "q0"

        elif estado == "q_num":
            while i < len(linea) and linea[i].isdigit():
                i += 1
            lexema = linea[inicio:i]
            tokens.append(f"<tk_entero,{lexema},{num_linea},{inicio+1}>")
            estado = "q0"

        elif estado == "q_string":
            while i < len(linea) and linea[i] != comilla:
                i += 1
            if i >= len(linea):
                error = f">>> Error léxico(linea:{num_linea},posicion:{i+1})"
                return ("ERROR", tokens, error)

            lexema = linea[inicio+1:i]
            tokens.append(f"<tk_cadena,\"{lexema}\",{num_linea},{inicio+1}>")
            i += 1
            estado = "q0"

    return tokens

def guardar_salida(tokens, archivo_salida="salida.txt"):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for t in tokens:
            f.write(t.rstrip("\n") + "\n")


if __name__ == "__main__":
    archivo_entrada = input("Ingrese el nombre del archivo .py a analizar: ").strip()
    tokens, hubo_error = analizar_archivo(archivo_entrada)
    guardar_salida(tokens)
    if hubo_error:
        print("Se detectó un error léxico, revise salida.txt.")
    else:
        print("Tokens guardados en salida.txt")
