
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
        # Función recursiva que va linea por linea
        oro_actual = mina_aux(gold, i, 0, n, m)
        oro_maximo = max(oro_maximo, oro_actual)

    return oro_maximo

def mina_aux(oro, x, y, filas, columnas):
    #condicón base
    if ((x < 0) or (x == filas) or (y == columnas)):
        return 0

    derecha_arriba = mina_aux(oro, x - 1, y + 1, filas, columnas)

    derecha = mina_aux(oro, x, y + 1, filas, columnas)

    derecha_abajo = mina_aux(oro, x + 1, y + 1, filas, columnas)

    # Retorna el maximo y almacena el valor
    return oro[x][y] + max(max(derecha_arriba, derecha_abajo), derecha)


#---------------------------------- Algoritmo Programacion Dinamica ----------------------------------
def mina_pd(valor, m, n):

    # Se crea la matriz
    matriz = [[0 for i in range(n)]
                 for j in range(m)]


    for filas in range(n - 1, -1, -1):
        for columnas in range(m):
            # se mueve a la siguiente selda a la derecha
            if (filas == n - 1):
                derecha = 0
            else:
                derecha = matriz[columnas][filas + 1]

            # se mueve a la siguiente selda a la derecha arriba
            if (columnas == 0 or filas == n - 1):
                derecha_arriba = 0
            else:
                derecha_arriba = matriz[columnas - 1][filas + 1]

            # se mueve a la siguiente selda a la derecha abajo
            if (columnas == m - 1 or filas == n - 1):
                derecha_abajo = 0
            else:
                derecha_abajo = matriz[columnas + 1][filas + 1]

            # Oro máximo recolectado al tomar cualquiera de los 3 caminos anteriores
            matriz[columnas][filas] = valor[columnas][filas] + max(derecha, derecha_arriba, derecha_abajo)

    """La cantidad máxima de oro
       recolectado será el máximo
       valor en la primera columna de todas las filas
    """
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