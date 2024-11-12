import pytest
from utils import Eigenvalue
import numpy as np

def test_eigenvalue():
    matrix = np.array([[1,6,3],[1/6,1,1/2],[1/3,2,1]])
    e = Eigenvalue()

    e.obtain_eigenvector_normalized(matrix)
