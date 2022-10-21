import numpy as np
import sys
import os
import time

def removeFile():
    try:
        os.remove("resultado_alineamiento.txt")
    except OSError:
        pass

# Este será un lector de archivos txt
def readFile(nombre_archivo):
    reader = open(nombre_archivo, 'r')
    file = reader.read()
    reader.close()
    return file

# Esta funcion se encargar de escribir en el archivo txt
def writeFile(text):
    reader = open("resultado_alineamiento.txt", 'a')
    if type(text) == type(list):
        for i in text:
            #reader.write("\n")
            i = str(i)
            reader.write(i)
    else:
        text = str(text)
        reader.write("\n")
        reader.write(text)
    reader.close()

# Esta función se encargará de separar los datos del archivo txt
def separarDatos(nombre_archivo):
    datos = readFile(nombre_archivo)
    datos = datos.split()
    datos2 = []
    for i in range(len(datos)):
        datos2.append(datos[i].split('\n'))
    return datos2


def alineamiento_pd(x: str, y: str):

    # initializing variables
    pxy = 1
    pgap = 2

    # table for storing optimal substructure answers
    tablaEnteros = np.zeros([len(x) + 1, len(y) + 1], dtype=int)  # int dp[m+1][len(y)+1] = {0};

    # initialising the table
    tablaEnteros[0:(len(x) + 1), 0] = [i * pgap for i in range(len(x) + 1)]
    tablaEnteros[0, 0:(len(y) + 1)] = [i * pgap for i in range(len(y) + 1)]

    # calculating the minimum penalty
    fila = 1
    while fila <= len(x):
        columna = 1
        while columna <= len(y):
            if x[fila - 1] == y[columna - 1]:
                tablaEnteros[fila][columna] = tablaEnteros[fila - 1][columna - 1]
            else:
                tablaEnteros[fila][columna] = min(tablaEnteros[fila - 1][columna - 1] + pxy,
                               tablaEnteros[fila - 1][columna] + pgap,
                               tablaEnteros[fila][columna - 1] + pgap)
            columna += 1
        fila += 1

    # Reconstructing the solution
    cantFilas = len(x)
    cantColumna = len(y)

    xPos = len(x) + len(y)
    yPos = len(x) + len(y)

    # Final answers for the respective strings
    repuestasFilas = np.zeros(len(x) + len(y) + 1, dtype=int)
    respuestasColumnas = np.zeros(len(x) + len(y) + 1, dtype=int)

    while not (cantFilas == 0 or cantColumna == 0):
        if x[cantFilas - 1] == y[cantColumna - 1]:
            repuestasFilas[xPos] = ord(x[cantFilas - 1])
            respuestasColumnas[yPos] = ord(y[cantColumna - 1])
            xPos -= 1
            yPos -= 1
            cantFilas -= 1
            cantColumna -= 1
        elif (tablaEnteros[cantFilas - 1][cantColumna - 1] + pxy) == tablaEnteros[cantFilas][cantColumna]:
            repuestasFilas[xPos] = ord(x[cantFilas - 1])
            respuestasColumnas[yPos] = ord(y[cantColumna - 1])
            xPos -= 1
            yPos -= 1
            cantFilas -= 1
            cantColumna -= 1
        elif (tablaEnteros[cantFilas - 1][cantColumna] + pgap) == tablaEnteros[cantFilas][cantColumna]:
            repuestasFilas[xPos] = ord(x[cantFilas - 1])
            respuestasColumnas[yPos] = ord('_')
            xPos -= 1
            yPos -= 1
            cantFilas -= 1
        elif (tablaEnteros[cantFilas][cantColumna - 1] + pgap) == tablaEnteros[cantFilas][cantColumna]:
            repuestasFilas[xPos] = ord('_')
            respuestasColumnas[yPos] = ord(y[cantColumna - 1])
            xPos -= 1
            yPos -= 1
            cantColumna -= 1

    while xPos > 0:
        if cantFilas > 0:
            cantFilas -= 1
            repuestasFilas[xPos] = ord(x[cantFilas])
            xPos -= 1
        else:
            repuestasFilas[xPos] = ord('_')
            xPos -= 1

    while yPos > 0:
        if cantColumna > 0:
            cantColumna -= 1
            respuestasColumnas[yPos] = ord(y[cantColumna])
            yPos -= 1
        else:
            respuestasColumnas[yPos] = ord('_')
            yPos -= 1

    # Since we have assumed the answer to be len(y)+m long,
    # we need to remove the extra gaps in the starting
    # id represents the index from which the arrays
    # repuestasFilas, respuestasColumnas are useful
    id = 1
    sumatoria = len(x) + len(y)
    while sumatoria >= 1:
        if (chr(respuestasColumnas[sumatoria]) == '_') and chr(repuestasFilas[sumatoria]) == '_':
            id = sumatoria + 1
            break

        sumatoria -= 1

    print("Los genes ya alineados son:")
    # X
    seleccionado= id
    x_seq = ""
    while seleccionado <= len(x) + len(y):
        x_seq += chr(repuestasFilas[seleccionado])
        seleccionado += 1
    print(f"Secuencia X: {x_seq}")

    # Y
    seleccionado = id
    y_seq = ""
    while seleccionado <= len(x) + len(y):
        y_seq += chr(respuestasColumnas[seleccionado])
        seleccionado += 1
    print(f"Secuencia Y: {y_seq}")

    score = 0
    for i in range(len(x_seq)):
        if x_seq[i] == y_seq[i]:
            score += 1
        elif x_seq[i] == '_' or y_seq[i] == '_':
            score -= 2
        else:
            score -= 1
    print("El puntaje de la secuencia es de: ", score)



def main():
    """
    Test the get_minimum_penalty function
    """
    # input strings
    print(len(sys.argv))
    datos = separarDatos("p1_alineamiento.txt")
    print(type(datos))
    print(datos)
    gene1 = datos[0][0]
    gene2 = datos[1][0]
    # initialising penalties of different types
    inicio = time.time()
    resultado = alineamiento_pd(gene1, gene2)
    #alignment_dp(gene1, gene2)
    final = time.time()
    print("El resultado es: ", resultado)
    print("Tiempo de ejecucion: ", final - inicio)
    exit(0)


main()
