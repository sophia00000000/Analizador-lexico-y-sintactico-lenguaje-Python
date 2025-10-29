def burbuja(lista):
    n = len(lista)
    for i in range(n - 1):
        #dksa
        for j in range(n - i - 1):
            #fdjsa
            if lista[j] > lista[j + 1]:
                # Intercambiar usando asignación múltiple (sin usar estructuras externas)
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


# Ejemplo de uso:
numeros = [5, 2, 9, 1, 5, 6]
ordenados = burbuja(numeros)
print("Lista ordenada:", ordenados)
