import unittest
import numpy as np
import sys
import os

# Add the path to the parent directory of the test directory to the Python path
test_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(test_dir)
sys.path.insert(0, parent_dir)

from verbose_chainsaw.nonnegdef import get_n_by_n


class TestMatrixProperties(unittest.TestCase):

    def test_symmetry(self): 
        m = get_n_by_n(5)
        self.assertTrue(np.allclose(m, m.conj().T))

    def test_non_neg_definite(self):
        m = get_n_by_n(6)
        self.assertTrue(np.all(np.linalg.eigvalsh(m) >= 0))

if __name__ == '__main__':
    unittest.main()
