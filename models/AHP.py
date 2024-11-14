import csv
from utils import Eigenvalue
import numpy as np


class AHP:
    def read_criterios(self, criterios_path='../data/criterios.csv'):
        criterios = []
        with open(criterios_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for row in reader:
                fila = []
                for cadena in row:
                    if '/' in cadena:
                        numerador, denominador = cadena.split("/")
                        number = float(numerador) / float(denominador)
                    else:
                        number = float(cadena)
                    fila.append(number)
                criterios.append(fila)

        self.criterios = np.array(criterios)
        self.num_criterios = np.shape(self.criterios)[0]

    def read_alternativas(self, alternatives_path='../data/alternatives.csv'):
        alternativas = []
        with open(alternatives_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            matriz_alternativas = []

            for row in reader:
                fila = []
                if row[0].startswith('A'):
                    # Header row
                    if alternativas:
                        matriz_alternativas.append(np.array(alternativas))
                    alternativas = []
                else:

                    for cadena in row:
                        if '/' in cadena:
                            numerador, denominador = cadena.split("/")
                            number = float(numerador) / float(denominador)
                        else:
                            number = float(cadena)
                        fila.append(number)
                    alternativas.append(fila)

            # Añadimos la ultima matriz
            matriz_alternativas.append(np.array(alternativas))
            self.alternativas = matriz_alternativas
            self.num_alternativas = np.shape(np.array(alternativas))[0]

    def __init__(self, criterios_path='./data/criterios.csv', alternatives_path='./data/alternatives.csv'):

        self.num_alternativas = None
        self.num_criterios = None
        self.criterios = None
        self.alternativas = None
        self.random_index = {3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


        self.read_criterios(criterios_path)

        self.read_alternativas(alternatives_path)

    def obtain_ranking(self):
        info_matrix = {}
        e = Eigenvalue()
        # Obtain the weights for the criterios matrix
        eigenvalue, weights_criterios = e.obtain_eigenvector_normalized(self.criterios)
        ci = (eigenvalue - self.num_criterios) / (self.num_criterios - 1)
        ri = self.random_index[self.num_criterios]
        info_matrix['C'] = [eigenvalue, ci, ri, ci / ri]
        # Obtain the weights for the alternatives
        weights_alternatives = []
        id = "AC"
        i = 1
        for alternatives in self.alternativas:
            eigenvalue, weight = e.obtain_eigenvector_normalized(alternatives)

            ci = (eigenvalue - self.num_alternativas) / (self.num_alternativas - 1)
            ri = self.random_index[self.num_alternativas]
            info_matrix[id + str(i)] = [eigenvalue, ci, ri, ci / ri]
            weights_alternatives.append(weight)
            i = i + 1
        weights_alternatives = np.array(weights_alternatives)

        ranking = np.dot(np.transpose(weights_alternatives), weights_criterios)
        ranking = [round(float(n),3) for n in ranking]

        print(f"Ranking: {ranking}. Info Consitency: {info_matrix}")
        return ranking, info_matrix
