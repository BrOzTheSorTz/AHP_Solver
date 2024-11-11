import sympy
import numpy as np


class Eigenvalue:
    def __init__(self, matrix, num):
        """
        :param matrix: a numpy matrix
        :param num:
        """
        self.matrix = matrix
        self.rows = num
        self.columns = num

    def run(self):
        """

        :return: Autovalor más grande no negativo y no imaginario
        """
        eigenvalues = np.linalg.eigvals(self.matrix)
        # Filtrar autovalores no negativos y reales
        real_non_negative = [value.real for value in eigenvalues if value.imag == 0 and value.real >= 0]
        # Retornar el mayor valor de la lista filtrada
        return max(real_non_negative) if real_non_negative else None
