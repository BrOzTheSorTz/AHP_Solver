import csv

import numpy as np
class AHP:
    def __init__(self,criterios_path = '../data/criterios.csv',alternatives_path = '../data/alternatives.csv'):

        criterios = []
        with open(criterios_path) as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            next(reader)
            for row in reader:
                fila = []
                for cadena in row:
                    if '/' in cadena:
                        numerador,denominador = cadena.split("/")
                        number = float(numerador)/float(denominador)
                    else:
                        number = float(cadena)
                    fila.append(number)
                criterios.append(fila)

        self.criterios = np.array(criterios)

        alternativas = []
        with open(alternatives_path) as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            matriz_alternativas = []

            for row in reader:
                if row[0].startswith('A'):
                    #Header row
                    if alternativas:
                        matriz_alternativas.append(alternativas)
                    alternativas = []
                else:
                    fila = []
                    for cadena in row:
                        if '/' in cadena:
                            numerador, denominador = cadena.split("/")
                            number = float(numerador) / float(denominador)
                        else:
                            number = float(cadena)
                        fila.append(number)
                alternativas.append(fila)

            #Añadimos la ultima matriz
            matriz_alternativas.append(alternativas)
            self.matrices_alternativas = matriz_alternativas
            # Mostrar las matrices de alternativas
            for idx, matriz in enumerate(matriz_alternativas):
                print(f"Alternativas del bloque {idx + 1}:")
                print(matriz)
                print()  # Salto de línea entre matrices