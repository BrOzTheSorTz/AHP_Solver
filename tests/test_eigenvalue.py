import pytest
from utils import Eigenvalue
import numpy as np

def test_eigenvalue():
    matrix = np.array([[1,3,7,8],[1/3,1,3,6],[1/7,1/3,1,3],[1/8,1/6,1/3,1]])
    e = Eigenvalue(matrix,4)

    eigenvalue=e.run()
    print(eigenvalue)