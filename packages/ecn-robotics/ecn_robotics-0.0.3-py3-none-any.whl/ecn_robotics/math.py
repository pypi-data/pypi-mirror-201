import copy
import numpy as np
from ecn_robotics.display import print_matrix


def idx_max(lst: list, start=0) -> int:
    """
    Search the index of the bigger absolute value in the given list.\n
    Code by Côte Geoffrey - 2023
    :param list lst: the list to search into
    :param int start: the index at which the search must begin
    :return: the index of the max value in the list
    """
    k = start
    m = np.fabs(lst[start])
    for i in range(start, len(lst), 1):
        if np.fabs(lst[i]) >= m:
            m = np.fabs(lst[i])
            k = i
    return k


def ech_red(matrix: np.ndarray, show_step=False) -> np.ndarray:
    """
    Compute the reduced row echelon form of the given matrix.\n
    Code by Côte Geoffrey - 2023
    :param matrix: the matrix from which the reduced row echelon form should be made
    :param show_step: whether we should display the intermediate step
    :return: the reduced row echelon form of the given matrix
    """
    # Make a copy of the matrix to work on
    out = copy.deepcopy(matrix)
    n = np.shape(out)
    r = 0
    if show_step: print_matrix(out, name=f"I")

    # We are iterating over the column
    for j in range(n[1]):
        # Finding the pivot value
        k = idx_max(out[:, j], r)
        if out[k, j] != 0:
            r += 1
            # Get the pivot to one
            out[k, :] = out[k, :] / out[k, j]
            if show_step: print_matrix(out, f"Pk{k}j{j}")

            # If the pivot is not on the right line, move it
            if k != r - 1:
                temp = copy.deepcopy(out[r - 1, :])
                out[r - 1, :] = out[k, :]
                out[k, :] = temp
                if show_step: print_matrix(out, f"Er{r - 1}k{k}")

            # Reduced the matrix by removing other values on the same column
            for i in range(0, n[0]):
                if i != r - 1:
                    out[i, :] = np.round(out[i, :] - out[r - 1, :] * out[i, j], 8)
                    if show_step: print_matrix(out, f"Ri{i}j{j}")
    return out
