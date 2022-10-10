
# Esta funicion sera la encargada de calcular el valor de la mochila
"""def mochila_fuerza_bruta(mochila):
    capacidad = mochila.capacidad
    objetos = mochila.posibles_objetos
    objetos_validos = []
    for i in objetos:
        #valida que cada objeto sobrepase la capacidad de la mochila
        if i.__get_peso__() <= capacidad:
            objetos_validos.append(i)
    lista_objetos = []
    resultado = []
    for i in objetos_validos:
        resultado_temporal = (mochila_fuerza_bruta_aux(objetos_validos, capacidad - i.__get_peso__(), lista_objetos))
        if beneficio_total(resultado_temporal) > beneficio_total(resultado):
            resultado = resultado_temporal
    return resultado
"""

"""def mochila_fuerza_bruta_aux(objetos_validos, peso_restante, lista_objetos):
    for i in objetos_validos:
        if peso_restante - i.__get_peso__() >= 0:
            lista_objetos.append(i)
            objetos_validos.remove(i)
            return mochila_fuerza_bruta_aux(objetos_validos, peso_restante - i.__get_peso__(), lista_objetos)
        else:
            return lista_objetos"""
