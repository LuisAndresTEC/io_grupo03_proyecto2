import sys
import os
import time
#import numpy as np
from operator import itemgetter

# Esta funcion se encargará de eliminar el archivo txt para borrar todo su contenido
def removeFile():
    try:
        os.remove("resultado_mochila.txt")
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
    reader = open("resultado_mochila.txt", 'a')
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
    return datos2

class objeto:
    def __init__(self, peso, valor):
        self.peso = peso
        self.valor = valor

    def __get_peso__(self):
        return self.peso

    def __get_valor__(self):
        return self.valor

class mochila:
    def __init__(self, atributos):
        self.capacidad = int(atributos[0][0])
        self.posibles_objetos= []
        for i in range(1, len(atributos)):
            self.posibles_objetos.append(objeto(int(atributos[i][0]), int(atributos[i][1])))

    def __get_capacidad__(self):
        return self.capacidad

    def __get_posibles_objetos__(self):
        return self.posibles_objetos





# Funcion simple que determina el pesos total de los elementos
def peso_total(objetos):
    return sum(i.__get_peso__() for i in objetos)

# Funcion que se encarga de sacar el total de valor de los elementos
def beneficio_total(objetos):
    return sum(i.__get_valor__() for i in objetos)


#--------------------------------------Mochila por medio de Fuerza Bruta--------------------------------------
def mochila_fuerza_bruta(objetos, capacidad):

    resultado = max(mochila_fuerza_bruta_aux(objetos, capacidad), key=beneficio_total)
    return resultado

def mochila_fuerza_bruta_aux(objetos, peso_restante):
    #Primero revisa que el objeto quepa en el peso restante
    objetos_validos = []
    for i in objetos:
        if i.__get_peso__() <= peso_restante:
            objetos_validos.append(i)

    resultado_final = []
    #Por cada objeto en los objetos validos se llama a la funcion recursiva con el peso restante menos el peso del objeto
    for i in objetos_validos:
        #Agrega a una lista los objetos restantes
        objetos_restantes = []
        for j in objetos_validos:
            if i != j:
                objetos_restantes.append(j)
        #Llama a la funcion recursiva con el peso restante menos el peso del objeto actual y los objetos restantes
        resultado_temporal = mochila_fuerza_bruta_aux(
            objetos_restantes, peso_restante - i.__get_peso__())
        #Si el resultado temporal es 0 entonces asume que es el resultado final
        if len(resultado_temporal) == 0:
            resultado_final.append([i])
        else:
            #Suma todos los anteriores resultados
            lista_anteriores = []
            for j in resultado_temporal:
                lista_anteriores.append([i] + j)
        #Si no es 0 entonces agrega el objeto actual a cada resultado temporal
            resultado_final.extend(lista_anteriores)
    return resultado_final



#--------------------------------------Mochila por medio de Programacion Dinamica--------------------------------------
def mochila_pd(peso_mochila, peso_objeto, valor, cantidad_objetos):

    if cantidad_objetos == 0 or peso_mochila == 0:
        return 0

    if (peso_objeto[cantidad_objetos - 1] > peso_mochila):
        objetos = "Los objetos de peso: " + str(peso_objeto) + " y valor: " + str(valor) + " se ingresaron en la mochila."
        writeFile(objetos)
        return mochila_pd(peso_mochila, peso_objeto, valor, cantidad_objetos - 1)

    else:
        return max(
            valor[cantidad_objetos - 1] + mochila_pd(peso_mochila - peso_objeto[cantidad_objetos - 1], peso_objeto, valor, cantidad_objetos - 1),
            mochila_pd(peso_mochila, peso_objeto, valor, cantidad_objetos - 1))


def main():
    if sys.argv[1] == "1":
        removeFile()
        datos = separarDatos(sys.argv[2])
        mochila_object = mochila(datos)
        inicio = time.time()
        resultado = mochila_fuerza_bruta(mochila_object.posibles_objetos, mochila_object.capacidad)
        final = time.time()
        pesos = []
        valores = []
        for i in resultado:
            pesos.append(i.__get_peso__())
        for i in resultado:
            valores.append(i.__get_valor__())
        writeFile("Fuerza Bruta")
        writeFile("Beneficio maximo: " + str(beneficio_total(resultado)))
        writeFile("Objetos seleccionados de peso: " + str(pesos) + " y valor: " + str(valores))
        writeFile("Tiempo de ejecucion: " + str(final - inicio))
        print("Ejecucion terminada correctamente")
        exit(0)
    elif sys.argv[1] == "2":
        removeFile()
        datos = separarDatos(sys.argv[2])
        mochila_object = mochila(datos)
        writeFile("Programacion Dinamica")
        inicio = time.time()
        resultado = mochila_pd(mochila_object.__get_capacidad__(),
                               [i.__get_peso__() for i in mochila_object.__get_posibles_objetos__()],
                               [i.__get_valor__() for i in mochila_object.__get_posibles_objetos__()],
                               len(mochila_object.__get_posibles_objetos__()))
        final = time.time()
        writeFile("Beneficio maximo: " + str(resultado))
        writeFile("Tiempo de ejecucion: " + str(final - inicio))
        print("Ejecucion terminada correctamente")
        exit(0)
    else:
        print("Opcion invalida")
        removeFile()
        writeFile("Opcion invalida seleccionada")
        exit(1)




main()