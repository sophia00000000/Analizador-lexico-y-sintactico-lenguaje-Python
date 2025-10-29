reglas = [
    "programa -> lista_declaraciones",
    "lista_declaraciones -> declaracion lista_declaraciones | ε",
    "declaracion  -> declaracion_clase | declaracion_funcion | sentencia",

    "declaracion_clase -> class id herencia_clase tk_dos_puntos TABS cuerpo_clase ATRAS",
    "herencia_clase -> tk_par_izq id tk_par_der | ε",
    "cuerpo_clase -> lista_declaraciones",

    "declaracion_funcion -> def id tk_par_izq parametros tk_par_der tipo_funcion tk_dos_puntos TABS bloque ATRAS",
    "parametros -> parametro parametros' | ε",
    "parametros' -> tk_coma parametro parametros' | ε",
    "parametro -> id tipo_opcional",
    "tipo_opcional -> tk_dos_puntos tipo | ε",
    "tipo_funcion -> tk_ejecuta tipo | ε",
    "tipo -> id | str | bool | object | tk_cua_izq tipo tk_cua_der | tk_cadena",

    "bloque -> tk_nueva_linea bloque | sentencia bloque' | ε",
    "bloque' -> tk_nueva_linea bloque' | sentencia bloque' | ε",

    "sentencia -> id sentencia_id' | sentencia_if | sentencia_while | sentencia_for | sentencia_print | sentencia_return | break tk_nueva_linea",
    
    "sentencia_id' -> indices_atributos sentencia_post_acceso",
    "indices_atributos -> tk_cua_izq expresion tk_cua_der indices_atributos | tk_punto id indices_atributos | ε",
    "sentencia_post_acceso -> tk_asig expresion_lista tk_nueva_linea | tk_dos_puntos tipo tk_asig expresion tk_nueva_linea | tk_par_izq argumentos tk_par_der tk_nueva_linea | tk_coma lista_targets tk_asig expresion_lista tk_nueva_linea | tk_nueva_linea",
    
    "lista_targets -> target mas_targets",
    "mas_targets -> tk_coma target mas_targets | ε",
    "target -> id indices_atributos",
    
    "expresion_lista -> expresion expresion_lista'",
    "expresion_lista' -> tk_coma expresion expresion_lista' | ε",

    "sentencia_expresion -> expresion tk_nueva_linea",
    "sentencia_return -> return expresion tk_nueva_linea",
    "sentencia_print -> print tk_par_izq lista_print tk_par_der tk_nueva_linea",
    "lista_print -> expresion lista_print' | ε",
    "lista_print' -> tk_coma expresion lista_print' | ε",
    "sentencia_if -> if condicion tk_dos_puntos cuerpo_if else_opcional",
    "cuerpo_if -> TABS bloque ATRAS | sentencia_simple",
    "sentencia_simple -> break tk_nueva_linea | return expresion tk_nueva_linea | id sentencia_id' | sentencia_print",
    "else_opcional -> else tk_dos_puntos cuerpo_else | ε",
    "cuerpo_else -> TABS bloque ATRAS | sentencia_simple",
    "sentencia_while -> while condicion tk_dos_puntos cuerpo_while",
    "cuerpo_while -> TABS bloque ATRAS | sentencia_simple",
    "sentencia_for -> for id in expresion tk_dos_puntos cuerpo_for",
    "cuerpo_for -> TABS bloque ATRAS | sentencia_simple ",

    # Condiciones con operadores lógicos
    "condicion -> expresion_logica",
    "expresion_logica -> expresion_or",
    "expresion_or -> expresion_and expresion_or'",
    "expresion_or' -> or expresion_and expresion_or' | ε",
    "expresion_and -> expresion_not expresion_and'",
    "expresion_and' -> and expresion_not expresion_and' | ε",
    "expresion_not -> not expresion_not | expresion_relacional",
    "expresion_relacional -> expresion expresion_relacional'",
    "expresion_relacional' -> operador_rel expresion | ε",
    "operador_rel -> tk_mayor | tk_menor | tk_igual | tk_distinto | tk_mayor_igual | tk_menor_igual",

    # Expresiones aritméticas
    "expresion -> termino expresion'",
    "expresion' -> tk_suma termino expresion' | tk_resta termino expresion' | ε",
    "termino -> factor termino'",
    "termino' -> tk_mul factor termino' | tk_div factor termino' | tk_mod factor termino' | ε",

    # Factor con soporte para índices y atributos
    "factor -> tk_par_izq expresion tk_par_der | tk_entero | tk_cadena | True | False | None | id factor_post | lista",
    "factor_post -> tk_cua_izq expresion tk_cua_der factor_post | tk_punto id factor_post | tk_par_izq argumentos tk_par_der | ε",

    # Listas
    "lista -> tk_cua_izq elementos tk_cua_der",
    "elementos -> expresion elementos' | ε",
    "elementos' -> tk_coma expresion elementos' | ε",

    "llamada -> id llamada'",
    "llamada' -> tk_par_izq argumentos tk_par_der | tk_punto id tk_par_izq argumentos tk_par_der | ε",

    "argumentos -> expresion argumentos' | ε",
    "argumentos' -> tk_coma expresion argumentos' | ε"
]

terminales = [
    'id','class','def','return','print','if','else','while','for','in',
    'str','bool','object','True','False','None',
    'tk_asig','tk_dos_puntos','tk_coma','tk_par_izq','tk_par_der',
    'tk_mayor','tk_menor','tk_igual','tk_distinto','tk_mayor_igual','tk_menor_igual',
    'tk_suma','tk_resta','tk_mul','tk_div','tk_punto','tk_cadena','tk_entero',
    'tk_nueva_linea','tk_ejecuta','TABS','ATRAS','tk_cua_izq','tk_cua_der', 'tk_mod',
    'and', 'or', 'not', 'break'
]

producciones = {}
# convierte la lista de reglas en una estructura más manejable (diccionario).
for r in reglas:
    if "->" not in r:
        continue
    izquierda, derecha = r.split("->", 1)
    A = izquierda.strip()
    A = A.replace("'", "'").replace("'", "'").strip()

    if A not in producciones:
        producciones[A] = []

    opciones = [op.strip() for op in derecha.strip().split("|")]
    for op in opciones:
        symbols = [s.replace("'", "'").replace("'", "'").strip() for s in op.split() if s.strip() != ""]
        producciones[A].append(symbols)

no_terminales  = set(producciones.keys())

PRIMEROS = {}
SIGUIENTES = {}

def primeros(simbolo):
    if simbolo in terminales:
        return {simbolo}
    if simbolo == "ε":
        return {"ε"}
    resultado = set()
    for prod in producciones[simbolo]:
        for s in prod:
            resultado |= (primeros(s) - {"ε"})
            if "ε" not in primeros(s):
                break
        else:
            resultado.add("ε")
    return resultado

def calcular_primeros():
    cambio = True
    while cambio:
        cambio = False
        for nt in no_terminales:
            if nt not in PRIMEROS:
                PRIMEROS[nt] = set()
            ant = set(PRIMEROS[nt])
            for prod in producciones[nt]:
                for s in prod:
                    PRIMEROS[nt] |= (PRIMEROS[s] if s in PRIMEROS else primeros(s)) - {"ε"}
                    if "ε" not in (PRIMEROS[s] if s in PRIMEROS else primeros(s)):
                        break
                else:
                    PRIMEROS[nt].add("ε")
            if ant != PRIMEROS[nt]:
                cambio = True

def calcular_siguientes():
    for nt in no_terminales:
        SIGUIENTES[nt] = set()
    SIGUIENTES["programa"].add("$")

    cambio = True
    while cambio:
        cambio = False
        for A, prods in list(producciones.items()):
            for prod in prods:
                simbolos = prod if isinstance(prod, list) else str(prod).split()

                for i, B in enumerate(simbolos):
                    if B not in no_terminales:
                        continue

                    beta = simbolos[i+1:] if i+1 < len(simbolos) else []

                    primeros_beta = set()
                    if beta:
                        for s in beta:
                            primeros_s = PRIMEROS[s] if s in PRIMEROS else primeros(s)
                            primeros_beta |= (primeros_s - {"ε"})
                            if "ε" in primeros_s:
                                continue
                            else:
                                break
                        else:
                            primeros_beta.add("ε")
                    else:
                        primeros_beta.add("ε")

                    ant_len = len(SIGUIENTES[B])

                    SIGUIENTES[B] |= (primeros_beta - {"ε"})

                    if not beta or "ε" in primeros_beta:
                        SIGUIENTES[B] |= SIGUIENTES[A]

                    if len(SIGUIENTES[B]) != ant_len:
                        cambio = True

tabla = {}

def construir_tabla():
    tabla.clear()
    for A, prods in producciones.items():
        if A not in tabla:
            tabla[A] = {}
        for prod in prods:
            simbolos = prod if isinstance(prod, list) else str(prod).split()

            primeros_alpha = set()
            if not simbolos:
                primeros_alpha.add("ε")
            else:
                for s in simbolos:
                    primeros_s = PRIMEROS[s] if s in PRIMEROS else primeros(s)
                    primeros_alpha |= (primeros_s - {"ε"})
                    if "ε" in primeros_s:
                        continue
                    else:
                        break
                else:
                    primeros_alpha.add("ε")

            for t in (primeros_alpha - {"ε"}):
                if t in tabla[A] and tabla[A][t] != simbolos:
                    print(f"CONFLICTO LL(1) en {A} con token {t}\n   Producción existente: {tabla[A][t]}\n   Nueva producción: {simbolos}\n")
                tabla[A][t] = simbolos

            if "ε" in primeros_alpha:
                for b in SIGUIENTES[A]:
                    if b in tabla[A] and tabla[A][b] != simbolos:
                        print(f"CONFLICTO LL(1) (ε) en {A} con token {b}\n   Producción existente: {tabla[A][b]}\n   Nueva producción: {simbolos}\n")
                    tabla[A][b] = simbolos

def leer_tokens(nombre_archivo="salida.txt"):
    tokens = []
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or not linea.startswith("<"):
                continue
            partes = linea[1:-1].split(",")
            if len(partes) == 4:
                tipo = partes[0]
                lexema = partes[1]
                linea_num = int(partes[2])
                col = int(partes[3])
            elif len(partes) == 3:
                tipo = partes[0]
                lexema = partes[0]
                linea_num = int(partes[1])
                col = int(partes[2])
            else:
                continue
            tokens.append({"tipo": tipo, "lexema": lexema, "linea": linea_num, "col": col})
    tokens.append({"tipo": "$", "lexema": "$", "linea": 9999, "col": 9999})
    return tokens

mapa_simbolos = {
    "tk_par_izq": "(", "tk_par_der": ")", "tk_dos_puntos": ":",
    "tk_coma": ",", "tk_punto": ".", "tk_asig": "=",
    "tk_mayor": ">", "tk_menor": "<", "tk_igual": "==", "tk_distinto": "!=",
    "tk_mayor_igual": ">=", "tk_menor_igual": "<=", "tk_suma": "+", "tk_resta": "-",
    "tk_mul": "*", "tk_div": "/", "tk_cadena": "cadena", "tk_entero": "entero",
    "tk_nueva_linea": "\\n", "tk_ejecuta": "->", "TABS": "indentación", "ATRAS": "dedentación",
    "True": "True", "False": "False", "None": "None", "tk_cua_izq": "[", "tk_cua_der": "]", 
    "tk_mod": "%", "and": "and", "or": "or", "not": "not", "break": "break"
}

def analizador_sintactico(tokens, tabla, simbolo_inicial="programa"):
    pila = ["$", simbolo_inicial]
    index = 0

    while pila:
        tope = pila[-1]
        actual = tokens[index]["tipo"]

        if tope == "$" and actual == "$":
            print("Análisis sintáctico completado sin errores.")
            return

        if tope in terminales or tope == "$":
            if tope == actual:
                pila.pop()
                index += 1
            else:
                token = tokens[index]
                esperado = mapa_simbolos.get(tope, tope)
                encontrado = mapa_simbolos.get(token["tipo"], token["lexema"])
                print(f"<{token['linea']},{token['col']}> Error sintáctico: se encontro: \"{encontrado}\"; se esperaba: \"{esperado}\".")
                return
        else:
            if tope in tabla and actual in tabla[tope]:
                prod = tabla[tope][actual]
                pila.pop()
                if prod != ["ε"]:
                    for s in reversed(prod):
                        pila.append(s)
            else:
                token = tokens[index]
                esperados = [mapa_simbolos.get(x, x) for x in tabla.get(tope, {}).keys()]
                encontrados = mapa_simbolos.get(token["tipo"], token["lexema"])

                # Detección de error de indentación
                if "dedentación" in esperados and token["tipo"] not in ("ATRAS", "$"):
                    print(f"<{token['linea']},{token['col']}> Error sintáctico: dedentación incorrecta (se esperaba reducir el nivel de indentación antes de '{encontrados}').")
                    return

                if token["tipo"] == "TABS" and "indentación" not in esperados:
                    print(f"<{token['linea']},{token['col']}> Error sintáctico: falla de indentación.")
                    return

                # Mensaje general
                lista_esp = ",".join(f"\"{e}\"" for e in esperados)
                print(f"<{token['linea']},{token['col']}> Error sintáctico: se encontró: \"{encontrados}\"; se esperaba: {lista_esp}.")
                return


if __name__ == "__main__":
    print("Calculando PRIMEROS...")
    calcular_primeros()
    print("Calculando SIGUIENTES...")
    calcular_siguientes()
    print("Construyendo tabla LL(1)...")
    construir_tabla()
    print("Iniciando análisis sintáctico...\n")
    tokens = leer_tokens("salida.txt")
    analizador_sintactico(tokens, tabla, "programa")