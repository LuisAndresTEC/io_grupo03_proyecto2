import numpy as np
import sys
import os
import time

"""
Estas funciones son las encargadas del proceso de lectura y escritura de los archivos de entradas 
de datos y de salida de resultados.
"""

#Función que eliman el archivo de resultados previo a la formualción de un nuevo resultado
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


""""
Descripción: Función encargada de aplicar el algoritmo de alineamiento de genes
Entradas: Una cadena de genes X y otra cadena de genes Y
Salidas: La solución óptima del alineamiento de genes
"""
def alineamiento(x: str, y: str):

    pxy = 1
    pgap = 2

    # tabla para almacenar las posibles soluciones óptimas
    tablaEnteros = np.zeros([len(x) + 1, len(y) + 1], dtype=int)  # int dp[m+1][len(y)+1] = {0};

    # Se inicializa la tabla de enteros
    tablaEnteros[0:(len(x) + 1), 0] = [i * pgap for i in range(len(x) + 1)]
    tablaEnteros[0, 0:(len(y) + 1)] = [i * pgap for i in range(len(y) + 1)]

    # Se calcula la minima penalidad
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

    # Se reestructura la solución
    cantFilas = len(x)
    cantColumna = len(y)

    xPos = len(x) + len(y)
    yPos = len(x) + len(y)

    # Respuestas finales para el alineamiento
    repuestasFilas = np.zeros(len(x) + len(y) + 1, dtype=int)
    respuestasColumnas = np.zeros(len(x) + len(y) + 1, dtype=int)

    # mientras que no se haya procesado toda la matriz
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

    """
    Como hemos supuesto que la respuesta es len(y)+m de largo,
    necesitamos eliminar los espacios adicionales en el inicio
    id representa el índice del que provienen las matrices
    respuestasFilas, respuestasColumnas son útiles
    """
    id = 1
    sumatoria = len(x) + len(y)
    while sumatoria >= 1:
        if (chr(respuestasColumnas[sumatoria]) == '_') and chr(repuestasFilas[sumatoria]) == '_':
            id = sumatoria + 1
            break

        sumatoria -= 1


    # X
    seleccionado= id
    x_seq = ""
    while seleccionado <= len(x) + len(y):
        x_seq += chr(repuestasFilas[seleccionado])
        seleccionado += 1

    # Y
    seleccionado = id
    y_seq = ""
    while seleccionado <= len(x) + len(y):
        y_seq += chr(respuestasColumnas[seleccionado])
        seleccionado += 1

    score = 0
    for i in range(len(x_seq)):
        if x_seq[i] == y_seq[i]:
            score += 1
        elif x_seq[i] == '_' or y_seq[i] == '_':
            score -= 2
        else:
            score -= 1

    return x_seq, y_seq, score



def main():
    removeFile()
    datos = separarDatos(sys.argv[1])
    gene1 = datos[0][0]
    gene2 = datos[1][0]
    inicio = time.time()
    resultado = alineamiento(gene1, gene2)
    final = time.time()
    writeFile("Los genes ya alineados son:")
    writeFile("El resultado es: ")
    writeFile(resultado[0])
    writeFile(resultado[1])
    writeFile("El puntaje es: " + str(resultado[2]))
    writeFile("Tiempo de ejecucion: " + str(final - inicio))
    exit(0)


main()
