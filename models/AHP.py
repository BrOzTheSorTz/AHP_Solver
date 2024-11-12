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

    def __init__(self, criterios_path='./data/criterios.csv', alternatives_path='./data/alternatives.csv'):

        self.criterios = None
        self.alternativas = None

        self.read_criterios(criterios_path)
        self.read_alternativas(alternatives_path)

    def obtain_ranking(self):

        e = Eigenvalue()
        # Obtain the weights for the criterios matrix
        weights_criterios = e.obtain_eigenvector_normalized(self.criterios)

        # Obtain the weights for the alternatives
        weights_alternatives = []
        for alternatives in self.alternativas:
            weight = e.obtain_eigenvector_normalized(alternatives)
            weights_alternatives.append(weight)
        weights_alternatives = np.array(weights_alternatives)

        ranking = np.dot(np.transpose(weights_alternatives),weights_criterios)

        print(f"Ranking: {ranking}")
        return ranking


