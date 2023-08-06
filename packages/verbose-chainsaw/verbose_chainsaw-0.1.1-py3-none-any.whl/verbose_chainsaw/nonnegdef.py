import numpy as np
from numpy.typing import ArrayLike 


def get_n_by_n(n: int) -> ArrayLike:
    """
    Parameters:
      n: int, the size of the n x n matrix
    Returns:
      An n x n matrix with eigenvalues of random phase on the unit circle.
      nonnegative definite, symmetric.
    """

    # Sample random phasors
    phases = np.random.uniform(0, 2*np.pi, size=(n,))
    eigenvalues = np.exp(1j * phases)

    # Construct a symmetric positive definite matrix with the specified eigenvalues
    Q = np.random.randn(n, n) + 1j * np.random.randn(n, n) # Generate random matrix
    S = Q @ Q.conj().T # Construct symmetric positive definite matrix
    eigvals, eigvecs = np.linalg.eigh(S) # Compute eigenvalue decomposition

    # Construct a diagonalizable matrix with the specified eigenvalues
    eigmat = eigvecs @ np.diag(eigenvalues) @ eigvecs.conj().T # Construct matrix

    # Ensure that eigmat is symmetric and non-negative definite
    eigmat = 0.5 * (eigmat + eigmat.conj().T) # Ensure symmetry
    eigmat = np.real_if_close(eigmat) # Ensure real values
    eigmat = eigmat @ eigmat.conj().T # Ensure non-negative definite
    return eigmat
