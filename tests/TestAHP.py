import unittest
import numpy as np
from models import AHP


class TestAHP(unittest.TestCase):

    def setUp(self):


        # Datos que esperamos que contenga la matriz, para comparar
        self.expected_matrix = np.array([
            [1, 3, 7, 8],
            [1 / 3, 1, 3, 6],
            [1 / 7, 1 / 3, 1, 3],
            [1 / 8, 1 / 6, 1 / 3, 1]
        ])
        self.alternatives_matrix = np.array([[[1,8,6],[1/8,1,1/3],[1/6,3,1]],[[1,5,1/3],[1/5,1,1/7],[3,7,1]]])
    def test_criterios_alternatives_loading(self):
        # Instancia de la clase AHP usando el archivo de prueba
        ahp_instance = AHP()

        # Verifica que self.criterios tenga los valores esperados
        np.testing.assert_array_almost_equal(
            ahp_instance.criterios,
            self.expected_matrix,
            decimal=5,
            err_msg="La matriz 'criterios' no coincide con los valores esperados"
        )

        np.testing.assert_array_almost_equal(
            ahp_instance.alternativas,
            self.alternatives_matrix
        )



# Ejecutar el test solo si se ejecuta el archivo de pruebas directamente
if __name__ == '__main__':
    unittest.main()
