
import sys
import os
import time

def removeFile():
    try:
        os.remove("resultado_mina.txt")
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
    reader = open("resultado_mina.txt", 'a')
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
        datos2.append(datos[i].split(','))
    for i in range(len(datos2)):
        for j in range(len(datos2[i])):
            datos2[i][j] = int(datos2[i][j])
    return datos2

#---------------------------------- Algoritmo Fuerza Bruta ----------------------------------
def mina_fuerza_bruta(gold, n, m):
    oro_maximo = 0

    for i in range(n):
        # Recursive function call for  ith row.
        oro_actual = mina_aux(gold, i, 0, n, m)
        oro_maximo = max(oro_maximo, oro_actual)

    return oro_maximo

def mina_aux(oro, x, y, filas, columnas):
    # Base condition.
    if ((x < 0) or (x == filas) or (y == columnas)):
        return 0

    derecha_arriba = mina_aux(oro, x - 1, y + 1, filas, columnas)

    derecha = mina_aux(oro, x, y + 1, filas, columnas)

    derecha_abajo = mina_aux(oro, x + 1, y + 1, filas, columnas)

    # Return the maximum and store the value
    return oro[x][y] + max(max(derecha_arriba, derecha_abajo), derecha)


#---------------------------------- Algoritmo Programacion Dinamica ----------------------------------
def mina_pd(valor, m, n):
    # Create a table for storing
    # intermediate results
    # and initialize all cells to 0.
    # The first row of
    # goldMineTable gives the
    # maximum gold that the miner
    # can collect when starts that row
    matriz = [[0 for i in range(n)]
                 for j in range(m)]

    for columnas in range(n - 1, -1, -1):
        for filas in range(m):

            # Gold collected on going to
            # the cell on the right(->)
            if (columnas == n - 1):
                derecha = 0
            else:
                derecha = matriz[filas][columnas + 1]

            # Gold collected on going to
            # the cell to right up (/)
            if (filas == 0 or columnas == n - 1):
                derecha_arriba = 0
            else:
                derecha_arriba = matriz[filas - 1][columnas + 1]

            # Gold collected on going to
            # the cell to right down (\)
            if (filas == m - 1 or columnas == n - 1):
                derecha_abajo = 0
            else:
                derecha_abajo = matriz[filas + 1][columnas + 1]

            # Max gold collected from taking
            # either of the above 3 paths
            matriz[filas][columnas] = valor[filas][columnas] + max(derecha, derecha_arriba, derecha_abajo)

    # The max amount of gold
    # collected will be the max
    # value in first column of all rows
    resultado = matriz[0][0]
    for i in range(1, m):
        resultado = max(resultado, matriz[i][0])

    return resultado





def main():
    if sys.argv[1] == "1":
        removeFile()
        datos = separarDatos(sys.argv[2])
        inicio = time.time()
        resultado = mina_fuerza_bruta(datos, len(datos), len(datos[0]))
        final = time.time()
        writeFile("Fuerza Bruta")
        writeFile("El resultado es: " + str(resultado))
        writeFile("Tiempo de ejecucion: " + str(final - inicio))
        print("Ejecucion terminada correctamente")
        exit(0)
    elif sys.argv[1] == "2":
        removeFile()
        datos = separarDatos(sys.argv[2])
        inicio = time.time()
        resultado = mina_pd(datos, len(datos), len(datos[0]))
        final = time.time()
        writeFile("Programacion Dinamica")
        writeFile("El resultado es: " + str(resultado))
        writeFile("Tiempo de ejecucion: " + str(final - inicio))
        print("Ejecucion terminada correctamente")
        exit(0)
    else:
        print("Opcion invalida")
        removeFile()
        writeFile("Opcion invalida seleccionada")
        exit(1)



main()