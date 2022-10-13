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



def get_minimum_penalty(x: str, y: str, pxy: int, pgap: int):
    """
    Function to find out the minimum penalty

    :param x: pattern X
    :param y: pattern Y
    :param pxy: penalty of mis-matching the characters of X and Y
    :param pgap: penalty of a gap between pattern elements
    """

    # initializing variables
    i = 0
    j = 0

    # pattern lengths
    m = len(x)
    n = len(y)

    # table for storing optimal substructure answers
    dp = np.zeros([m + 1, n + 1], dtype=int)  # int dp[m+1][n+1] = {0};

    # initialising the table
    dp[0:(m + 1), 0] = [i * pgap for i in range(m + 1)]
    dp[0, 0:(n + 1)] = [i * pgap for i in range(n + 1)]

    # calculating the minimum penalty
    i = 1
    while i <= m:
        j = 1
        while j <= n:
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + pxy,
                               dp[i - 1][j] + pgap,
                               dp[i][j - 1] + pgap)
            j += 1
        i += 1

    # Reconstructing the solution
    l = n + m  # maximum possible length
    i = m
    j = n

    xpos = l
    ypos = l

    # Final answers for the respective strings
    xans = np.zeros(l + 1, dtype=int)
    yans = np.zeros(l + 1, dtype=int)

    while not (i == 0 or j == 0):
        # print(f"i: {i}, j: {j}")
        if x[i - 1] == y[j - 1]:
            xans[xpos] = ord(x[i - 1])
            yans[ypos] = ord(y[j - 1])
            xpos -= 1
            ypos -= 1
            i -= 1
            j -= 1
        elif (dp[i - 1][j - 1] + pxy) == dp[i][j]:

            xans[xpos] = ord(x[i - 1])
            yans[ypos] = ord(y[j - 1])
            xpos -= 1
            ypos -= 1
            i -= 1
            j -= 1

        elif (dp[i - 1][j] + pgap) == dp[i][j]:
            xans[xpos] = ord(x[i - 1])
            yans[ypos] = ord('_')
            xpos -= 1
            ypos -= 1
            i -= 1

        elif (dp[i][j - 1] + pgap) == dp[i][j]:
            xans[xpos] = ord('_')
            yans[ypos] = ord(y[j - 1])
            xpos -= 1
            ypos -= 1
            j -= 1

    while xpos > 0:
        if i > 0:
            i -= 1
            xans[xpos] = ord(x[i])
            xpos -= 1
        else:
            xans[xpos] = ord('_')
            xpos -= 1

    while ypos > 0:
        if j > 0:
            j -= 1
            yans[ypos] = ord(y[j])
            ypos -= 1
        else:
            yans[ypos] = ord('_')
            ypos -= 1

    # Since we have assumed the answer to be n+m long,
    # we need to remove the extra gaps in the starting
    # id represents the index from which the arrays
    # xans, yans are useful
    id = 1
    i = l
    while i >= 1:
        if (chr(yans[i]) == '_') and chr(xans[i]) == '_':
            id = i + 1
            break

        i -= 1

    # Printing the final answer
    print(f"Minimum Penalty in aligning the genes = {dp[m][n]}")
    print("The aligned genes are:")
    # X
    i = id
    x_seq = ""
    while i <= l:
        x_seq += chr(xans[i])
        i += 1
    print(f"X seq: {x_seq}")

    # Y
    i = id
    y_seq = ""
    while i <= l:
        y_seq += chr(yans[i])
        i += 1
    print(f"Y seq: {y_seq}")

from collections import deque


def all_alignments(x, y):
    """Return an iterable of all alignments of two
    sequences.

    x, y -- Sequences.
    """

    def F(x, y):
        """A helper function that recursively builds the
        alignments.

        x, y -- Sequence indices for the original x and y.
        """
        if len(x) == 0 and len(y) == 0:
            yield deque()

        scenarios = []
        if len(x) > 0 and len(y) > 0:
            scenarios.append((x[0], x[1:], y[0], y[1:]))
        if len(x) > 0:
            scenarios.append((x[0], x[1:], None, y))
        if len(y) > 0:
            scenarios.append((None, x, y[0], y[1:]))

        # NOTE: "xh" and "xt" stand for "x-head" and "x-tail",
        # with "head" being the front of the sequence, and
        # "tail" being the rest of the sequence. Similarly for
        # "yh" and "yt".
        for xh, xt, yh, yt in scenarios:
            for alignment in F(xt, yt):
                alignment.appendleft((xh, yh))
                yield alignment

    alignments = F(range(len(x)), range(len(y)))
    return map(list, alignments)

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
    mismatch_penalty = 3
    gap_penalty = 2
    inicio = time.time()
    resultado = all_alignments(gene1, gene2)
    #get_minimum_penalty(gene1, gene2, mismatch_penalty, gap_penalty)
    final = time.time()
    print("El resultado es: ", list(resultado))
    print("Tiempo de ejecucion: ", final - inicio)
    exit(0)







main()
