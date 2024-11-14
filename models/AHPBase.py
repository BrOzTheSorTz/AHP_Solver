import csv
import numpy as np
from utils import Eigenvalue


# Clase base para manejar la carga de datos CSV
class AHPBase:
    def __init__(self, criterios_path='./data/criterios.csv', alternatives_path='./data/alternatives.csv'):
        self.num_alternativas = None
        self.num_criterios = None
        self.criterios = None
        self.alternativas = None
        self.random_index = {3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        self.read_criterios(criterios_path)
        self.read_alternativas(alternatives_path)

    # Lee los criterios desde un archivo CSV
    def read_criterios(self, criterios_path):
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

    # Lee las alternativas desde un archivo CSV
    def read_alternativas(self, alternatives_path):
        alternativas = []
        with open(alternatives_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            matriz_alternativas = []

            for row in reader:
                fila = []
                if row[0].startswith('A'):  # Header row
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
            matriz_alternativas.append(np.array(alternativas))
            self.alternativas = matriz_alternativas
            self.num_alternativas = np.shape(np.array(alternativas))[0]

    # Método abstracto a implementar en cada clase hija
    def obtain_ranking(self):
        raise NotImplementedError("Subclasses should implement this method.")


# Clase hija para el método de autovalores
class AHPAutovalores(AHPBase):
    def obtain_ranking(self):
        info_matrix = {}
        e = Eigenvalue()
        # Pesos de la matriz de criterios usando autovalores
        eigenvalue, weights_criterios = e.obtain_eigenvector_normalized(self.criterios)
        ci = (eigenvalue - self.num_criterios) / (self.num_criterios - 1)
        ri = self.random_index[self.num_criterios]
        info_matrix['C'] = [eigenvalue, ci, ri, ci / ri]

        weights_alternatives = []
        id = "AC"
        i = 1
        for alternatives in self.alternativas:
            eigenvalue, weight = e.obtain_eigenvector_normalized(alternatives)
            ci = (eigenvalue - self.num_alternativas) / (self.num_alternativas - 1)
            ri = self.random_index[self.num_alternativas]
            info_matrix[id + str(i)] = [eigenvalue, ci, ri, ci / ri]
            weights_alternatives.append(weight)
            i += 1
        weights_alternatives = np.array(weights_alternatives)
        ranking = np.dot(np.transpose(weights_alternatives), weights_criterios)
        ranking = [round(float(n), 3) for n in ranking]

        print(f"Ranking: {ranking}. Info Consitency: {info_matrix}")
        return ranking, info_matrix


# Clase hija para el método aproximado
class AHPAproximado(AHPBase):
    def obtain_ranking(self):

        # Obtener pesos de los criterios
        weigths = []
        sum_total = 0.0
        print("CRITERIO ",self.num_criterios)
        for i in range(0,self.num_criterios):
            suma = sum(self.criterios[i])
            weigths.append(suma)
            sum_total = sum_total + suma

        weigths_norm = [num/sum_total for num in weigths]
        print(weigths_norm)
        weigths_norm_criterios = np.array(weigths_norm)

        # Obtener valores de las alternativas
        alts_weigths = []
        for alternativa in self.alternativas:
            weigths = []
            sum_total = 0.0
            for i in range(0, self.num_alternativas):
                suma = sum(alternativa[i])
                weigths.append(suma)
                sum_total = sum_total + suma

            weigths_norm = [num / sum_total for num in weigths]
            alts_weigths.append(weigths_norm)
        alts_weigths = np.array(alts_weigths)

        ranking = np.dot(np.transpose(alts_weigths), weigths_norm_criterios)
        ranking = [round(float(n), 3) for n in ranking]

        print(f"Ranking: {ranking}.")
        return ranking, {}



# Clase hija para el método de media geométrica
class AHPMediaGeometrica(AHPBase):
    def obtain_ranking(self):
        # Paso 1: Calcular media geométrica de los criterios
        criterios_pesos = []
        for i in range(self.num_criterios):
            # Producto de todos los elementos en la fila
            product = np.prod(self.criterios[i])
            # Raíz enésima (media geométrica)
            geometric_mean = product ** (1 / self.num_criterios)
            criterios_pesos.append(geometric_mean)

        # Paso 2: Normalizar los pesos de los criterios
        suma_total_criterios = sum(criterios_pesos)
        criterios_pesos_norm = np.array([peso / suma_total_criterios for peso in criterios_pesos])

        # Paso 3: Calcular media geométrica de las alternativas
        alts_pesos_normalizados = []
        for alternativa in self.alternativas:
            alt_pesos = []
            for i in range(self.num_alternativas):
                # Producto de todos los elementos en la fila
                product = np.prod(alternativa[i])
                # Raíz enésima (media geométrica)
                geometric_mean = product ** (1 / self.num_alternativas)
                alt_pesos.append(geometric_mean)

            # Normalizar los pesos de cada matriz de alternativas
            suma_total_alternativa = sum(alt_pesos)
            alt_pesos_norm = [peso / suma_total_alternativa for peso in alt_pesos]
            alts_pesos_normalizados.append(alt_pesos_norm)

        alts_pesos_normalizados = np.array(alts_pesos_normalizados)

        # Paso 4: Calcular el ranking final
        ranking = np.dot(np.transpose(alts_pesos_normalizados), criterios_pesos_norm)
        ranking = [round(float(n), 3) for n in ranking]

        print(f"Ranking: {ranking}.")
        return ranking, {}