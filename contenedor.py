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


#Esta funcion calculara mochila por medio de fuerza bruta
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

def main():
    print(len(sys.argv))
    datos = separarDatos("p1_mochila.txt")
    print(type(datos))
    print(datos)
    mochila_object = mochila(datos)
    inicio = time.time()
    resultado = mochila_fuerza_bruta(mochila_object.posibles_objetos, mochila_object.capacidad)
    final = time.time()
    beneficio = beneficio_total(resultado)
    peso = peso_total(resultado)
    print("el peso total es: ", peso)
    print("El beneficio total es: ", beneficio)
    for i in resultado:
        print(i.__get_peso__(), i.__get_valor__())
    print("Tiempo de ejecucion: ", final - inicio)
    exit(0)




main()