
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
def mina_pd(gold, m, n):
    # Create a table for storing
    # intermediate results
    # and initialize all cells to 0.
    # The first row of
    # goldMineTable gives the
    # maximum gold that the miner
    # can collect when starts that row
    goldTable = [[0 for i in range(n)]
                 for j in range(m)]

    for col in range(n - 1, -1, -1):
        for row in range(m):

            # Gold collected on going to
            # the cell on the right(->)
            if (col == n - 1):
                right = 0
            else:
                right = goldTable[row][col + 1]

            # Gold collected on going to
            # the cell to right up (/)
            if (row == 0 or col == n - 1):
                right_up = 0
            else:
                right_up = goldTable[row - 1][col + 1]

            # Gold collected on going to
            # the cell to right down (\)
            if (row == m - 1 or col == n - 1):
                right_down = 0
            else:
                right_down = goldTable[row + 1][col + 1]

            # Max gold collected from taking
            # either of the above 3 paths
            goldTable[row][col] = gold[row][col] + max(right, right_up, right_down)

    # The max amount of gold
    # collected will be the max
    # value in first column of all rows
    res = goldTable[0][0]
    for i in range(1, m):
        res = max(res, goldTable[i][0])

    return res





def main():
    print(len(sys.argv))
    datos = separarDatos("p2_mina.txt")
    print(type(datos[1][1]))
    print(datos)
    inicio = time.time()
    #resultado = mina_fuerza_bruta(datos, len(datos), len(datos[0]))
    resultado = mina_pd(datos, len(datos), len(datos[0]))
    final = time.time()
    print("El resultado es: ", resultado)
    print("Tiempo de ejecucion: ", final - inicio)
    exit(0)




main()